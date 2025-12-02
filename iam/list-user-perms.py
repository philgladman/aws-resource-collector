import boto3
import jmespath
import json
import os

iam = boto3.client('iam')

relative_folder_path = os.path.dirname(__file__)
input_filename = os.path.join(relative_folder_path, 'users.json')
f = open (input_filename, "r")
data = json.loads(f.read())

users_dir = os.path.join(relative_folder_path, 'users')
if not os.path.exists(users_dir):
    os.makedirs(users_dir)

for key,values in data.items():
    for value in values:
        policy_arn = iam.get_policy(PolicyArn=value)
        policy_default_version = jmespath.search('Policy.DefaultVersionId', policy_arn)

        policy = iam.get_policy_version(PolicyArn=value, VersionId=policy_default_version)
        policy_formatted = jmespath.search('PolicyVersion.Document', policy)
        output_filename = relative_folder_path + "/users/" + key + ".json"
        print(f"creating file with policy(s) for user: {key}")
        with open(output_filename, "a") as outfile:
            outfile.writelines("USER NAME: " + key)
            outfile.writelines("\n")
            outfile.writelines("POLICY ARN: " + value)
            outfile.writelines("\n")
            outfile.writelines(json.dumps(policy_formatted, indent=2, default=str))
            outfile.writelines("\n" * 3)
