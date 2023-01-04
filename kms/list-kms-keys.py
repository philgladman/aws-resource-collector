import boto3
from botocore.exceptions import ClientError
import jmespath
import json
import os

AWS_REGION = 'us-east-1'
kms = boto3.client('kms', region_name=AWS_REGION)

keys = kms.list_keys()
key_ids = jmespath.search('Keys[].KeyId', keys)
key_arns = jmespath.search('Keys[].KeyArn', keys)

def enabled_keys(key_ids):
    """Creates and returns list of AWS KMS keys that have a key state of enabled."""
    enabled_key_ids = []
    for i in key_ids:
        try:
            key_description = kms.describe_key(KeyId=i)
            key_state = jmespath.search('KeyMetadata.KeyState', key_description)
            if key_state == "Enabled":
                enabled_key_ids.append(i)
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDeniedException':
                print("access denied: ", i)
                continue
            else:
                print("Unexpected error: %s" % e)

    return enabled_key_ids

def get_cmks(enabled_key_ids):
    """Creates and returns a list of enabled AWS Customer Managed Keys"""
    list_of_cmks = []
    for i in enabled_key_ids:
        response = kms.describe_key(KeyId=i)
        key_manager = jmespath.search('KeyMetadata.KeyManager', response)
        if key_manager == 'CUSTOMER':
            list_of_cmks.append(i)
    
    return list_of_cmks

def get_cmk_policy(list_of_cmks): 
    """Creates a file for each AWS KMS key. Name of the file = key alias, and the file contents = kms key policy"""
    for cmk in list_of_cmks:
        alias = kms.list_aliases(KeyId=cmk)
        key_names = jmespath.search('Aliases[].AliasName', alias)
        for key_name in key_names:
            if key_name != "":
                key_name_alias = key_name.strip("alias/")
                try:
                    relative_folder_path = os.path.dirname(__file__)
                    output_filename = relative_folder_path + "/keys/" + key_name_alias + ".json"
                    with open(output_filename, "a") as outfile:
                        outfile.writelines("KEY_NAME: " + key_name_alias)
                        outfile.writelines("\n")
                        response = kms.get_key_policy(KeyId=cmk,PolicyName='default')
                        policy = jmespath.search('Policy', response)
                        outfile.writelines(policy)
                except:
                    print(key_name, "key alias has invlaid character")

if __name__ == '__main__':
    list_of_cmks = get_cmks(enabled_keys(key_ids))
    get_cmk_policy(list_of_cmks)