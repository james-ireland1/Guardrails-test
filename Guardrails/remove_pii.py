import boto3
import botocore
import json
import os
from dotenv import load_dotenv

load_dotenv()

def apply_guardrail(text):
    bedrock_runtime = boto3.client(
        'bedrock-runtime',
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
        region_name='eu-north-1')
    try:
        response = bedrock_runtime.apply_guardrail(
            guardrailIdentifier='43jbbow7bayq',
            guardrailVersion='DRAFT',
            source='INPUT',
            content=[
                {
                    'text': {
                        'text': text,
                        'qualifiers': ['guard_content']
                    }
                }
            ],
            outputScope='INTERVENTIONS'
        )
        print('Successfully applied guardrail with details:')
        print(json.dumps(response, indent=2))
        return response['outputs'][0]['text']
    except botocore.exceptions.ClientError as err:
        print('Failed while calling ApplyGuardrail API with RequestId = ' + err.response['ResponseMetadata']['RequestId'])
        raise err

def remove_pii(text):
    apply_guardrail(text)


test_text = 'My name is James. I work for Softwire at 62-64 Hills Road, Cambridge, CB2 1LA. My phone number is 07382594632 and my email address is james.ireland@softwire.com. You can also reach me on james.ireland at softwire.com. I log in using jamireadmin and use fhGtjdH4897 as my password.'

apply_guardrail(test_text)