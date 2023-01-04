import boto3
import jmespath
import json
import os

AWS_REGION = 'us-east-1'
iam = boto3.client('iam', region_name=AWS_REGION)

relative_folder_path = os.path.dirname(__file__)
input_filename = os.path.join(relative_folder_path, 'roles.json')
f = open (input_filename, "r")
data = json.loads(f.read())

for key,values in data.items():
    for value in values:
        policy_arn = iam.get_policy(PolicyArn=value)
        policy_default_version = jmespath.search('Policy.DefaultVersionId', policy_arn)

        policy = iam.get_policy_version(PolicyArn=value, VersionId=policy_default_version)
        policy_formatted = jmespath.search('PolicyVersion.Document', policy)
        output_filename = relative_folder_path + "/roles/" + key + ".json"
        with open(output_filename, "a") as outfile:
            outfile.writelines("ROLE NAME: " + key)
            outfile.writelines("\n")
            outfile.writelines("POLICY ARN: " + value)
            outfile.writelines("\n")
            outfile.writelines(json.dumps(policy_formatted, indent=2, default=str))
            outfile.writelines("\n" * 3)

