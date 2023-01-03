import boto3
import jmespath
import json

AWS_REGION = 'us-east-1'
iam = boto3.client('iam', region_name=AWS_REGION)

def get_role_name():
    roles = iam.list_roles()
    role_names = jmespath.search('Roles[].RoleName', roles)
    # role_names_list = []
    # for i in role_names:
    #     if "REPLACE" in i:
    #         role_names_list.append(i)

    # return role_names_list
    return role_names

def get_policy_arn(list_of_role_names):
    aws_roles = {}
    for role_name in list_of_role_names:
        role_perms = iam.list_attached_role_policies(RoleName=role_name)
        policy_arns = jmespath.search('AttachedPolicies[].PolicyArn', role_perms)
        aws_roles[role_name] = policy_arns
    return json.dumps(aws_roles, indent=2, default=str)

# print(get_policy_arn(get_role_name()))

if __name__ == "__main__":
    aws_role_policy_arn = get_policy_arn(get_role_name())
    with open("<REPLACE>/aws-resource-collector/iam/roles.json", "w") as outfile:
        outfile.write(aws_role_policy_arn)
