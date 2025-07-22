import boto3
import botocore
import json
import os
from dotenv import load_dotenv
from create_remove_pii_guardrail import create_guardrail
from remove_pii import apply_guardrail, remove_pii

load_dotenv()

def remove_pii_custom(text, pii_types=None):
    if pii_types is None:
        pii_types = []
    if len(pii_types) == 0:
        return remove_pii(text)
    else:
        guardrail_id, guardrail_version = create_guardrail('remove-pii-custom',pii_types)
        return apply_guardrail(text, guardrail_id, guardrail_version)


test_text = 'My name is James. I work for Softwire at 62-64 Hills Road, Cambridge, CB2 1LA. My phone number is 07382594632 and my email address is james.ireland@softwire.com. You can also reach me on james.ireland at softwire.com. I log in using jamireadmin and use fhGtjdH4897 as my password.'

print(remove_pii_custom(test_text,['PASSWORD','EMAIL']))