import boto3
import botocore
import json
import os
from dotenv import load_dotenv

load_dotenv()

pii_types = [
    'ADDRESS',
    'AGE',
    'NAME',
    'EMAIL',
    'PHONE',
    'USERNAME',
    'PASSWORD',
    'DRIVER_ID',
    'LICENSE_PLATE',
    'VEHICLE_IDENTIFICATION_NUMBER',
    'CREDIT_DEBIT_CARD_CVV',
    'CREDIT_DEBIT_CARD_EXPIRY',
    'CREDIT_DEBIT_CARD_NUMBER',
    'PIN',
    'INTERNATIONAL_BANK_ACCOUNT_NUMBER',
    'SWIFT_CODE',
    'IP_ADDRESS',
    'MAC_ADDRESS',
    'URL',
    'AWS_ACCESS_KEY',
    'AWS_SECRET_KEY',
    'US_BANK_ACCOUNT_NUMBER',
    'US_BANK_ROUTING_NUMBER',
    'US_INDIVIDUAL_TAX_IDENTIFICATION_NUMBER',
    'US_PASSPORT_NUMBER',
    'US_SOCIAL_SECURITY_NUMBER',
    'CA_HEALTH_NUMBER',
    'CA_SOCIAL_INSURANCE_NUMBER',
    'UK_NATIONAL_HEALTH_SERVICE_NUMBER',
    'UK_NATIONAL_INSURANCE_NUMBER',
    'UK_UNIQUE_TAXPAYER_REFERENCE_NUMBER']

def list_guardrails():
    bedrock = boto3.client(
        'bedrock',
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
        region_name='eu-north-1')
    response = bedrock.list_guardrails()
    while response['nextToken']:
        response.append(bedrock.list_guardrails(nextToken=response['nextToken']))
    return response['guardrails']

def create_pii_entities_config(chosen_pii_types):
    if len(chosen_pii_types) < 1: chosen_pii_types = pii_types
    config = []
    for pii_type in chosen_pii_types:
        if pii_type in pii_types:
            config.append({
                'type': pii_type,
                'action': 'ANONYMIZE',
                'inputAction': 'ANONYMIZE',
                'inputEnabled': True,
                'outputAction': 'ANONYMIZE',
                'outputEnabled': True
            })
    print(config)
    return config

def create_guardrail(name, pii_types):
    bedrock = boto3.client(
        'bedrock',
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
        region_name='eu-north-1')
    pii_entities_config = create_pii_entities_config(pii_types)
    try:
        create_guardrail_response = bedrock.create_guardrail(
            name=name,
            sensitiveInformationPolicyConfig={
                'piiEntitiesConfig': pii_entities_config
            },
            blockedInputMessaging='Sorry, this input has been blocked.',
            blockedOutputsMessaging='Sorry, this output has been blocked.',
        )
        create_guardrail_response['createdAt'] = create_guardrail_response['createdAt'].strftime('%Y-%m-%d %H:%M:%S')
        print("Successfully created guardrail with details:")
        print(json.dumps(create_guardrail_response, indent=2))
        return create_guardrail_response['guardrailId'], create_guardrail_response['version']
    except botocore.exceptions.ClientError as err:
        print("Failed while calling CreateGuardrail API with RequestId = " + err.response['ResponseMetadata']['RequestId'])
        raise err