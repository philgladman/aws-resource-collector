import boto3
import jmespath
import json
import os

iam = boto3.client('iam')

def get_role_name():
    paginator = iam.get_paginator('list_roles')
    page_iterator = paginator.paginate(PaginationConfig={'PageSize': 50})
    role_names = []
    for page in page_iterator:
        role_names = jmespath.search('Roles[].RoleName', page) + role_names
    return role_names

def get_policy_arn(list_of_role_names):
    aws_roles = {}
    for role_name in list_of_role_names:
        print(f"Adding role to file: {role_name}")
        role_perms = iam.list_attached_role_policies(RoleName=role_name)
        policy_arns = jmespath.search('AttachedPolicies[].PolicyArn', role_perms)
        aws_roles[role_name] = policy_arns
    return json.dumps(aws_roles, indent=2, default=str)

if __name__ == "__main__":
    aws_role_policy_arn = get_policy_arn(get_role_name())
    relative_folder_path = os.path.dirname(__file__)
    output_filename = os.path.join(relative_folder_path, 'roles.json')
    with open(output_filename, "w") as outfile:
        outfile.write(aws_role_policy_arn)
