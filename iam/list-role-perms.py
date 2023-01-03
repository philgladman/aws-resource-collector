import boto3
import jmespath
import json

AWS_REGION = 'us-east-1'
iam = boto3.client('iam', region_name=AWS_REGION)

f = open ('<REPLACE>/aws-resource-collector/iam/roles.json', "r")
data = json.loads(f.read())

for key,values in data.items():
    for value in values:
        policy_arn = iam.get_policy(PolicyArn=value)
        policy_default_version = jmespath.search('Policy.DefaultVersionId', policy_arn)

        policy = iam.get_policy_version(PolicyArn=value, VersionId=policy_default_version)
        policy_formatted = jmespath.search('PolicyVersion.Document', policy)
        with open('<REPLACE>/aws-resource-collector/iam/roles/%s.json' % key, "a") as outfile:
            outfile.writelines("ROLE NAME: " + key)
            outfile.writelines("\n")
            outfile.writelines("POLICY ARN: " + value)
            outfile.writelines("\n")
            outfile.writelines(json.dumps(policy_formatted, indent=2, default=str))
            outfile.writelines("\n" * 3)

