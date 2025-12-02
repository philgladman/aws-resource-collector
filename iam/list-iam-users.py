import boto3
import jmespath
import json
import os

iam = boto3.client('iam')

def get_user_names():
    """Builds a list of all iam user accounts"""
    users = iam.list_users()
    user_names = jmespath.search('Users[].UserName', users)
    # user_names_list = []
    # for i in user_names:
    #     if "REPLACE" in i:
    #         user_names_list.append(i)

    # return user_names_list
    return user_names


def get_user_policies(user_names_list):
    """Takes list of iam user acconuts as input, and creates a dictionary that has each iam user, with all of its attached user policies"""
    aws_users = {}
    for user_name in user_names_list:
        user_policies = []
        attached_policy = iam.list_attached_user_policies(UserName=user_name)
        attached_policy_arn = jmespath.search('AttachedPolicies[].PolicyArn', attached_policy)
        user_policies += attached_policy_arn
        aws_users[user_name] = user_policies

    return aws_users


def get_group_policies(aws_users):    
    """Appends attached group polices to each user in the aws_users dictonary created in the get_user_policies function"""
    for user in aws_users:
        attached_groups = iam.list_groups_for_user(UserName=user)
        groups = jmespath.search('Groups[].GroupName', attached_groups)
        group_policies = []
        for group in groups:
            attached_group_policy = iam.list_attached_group_policies(GroupName=group)
            attached_group_policy_arn = jmespath.search('AttachedPolicies[].PolicyArn', attached_group_policy)
            group_policies += attached_group_policy_arn
        policies = group_policies + aws_users[user]
        aws_users[user] = policies

    return json.dumps(aws_users, indent=2, default=str)


if __name__ == "__main__":
    user_names_list = get_user_names()
    aws_users = get_user_policies(user_names_list)
    aws_user_policy_arn = get_group_policies(aws_users)
    relative_folder_path = os.path.dirname(__file__)
    output_filename = os.path.join(relative_folder_path, 'users.json')
    with open(output_filename, "w") as outfile:
        outfile.write(aws_user_policy_arn)
