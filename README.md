# aws-resource-collector
Python scripts to collect and document all IAM and KMS resources for an AWS Account.


### IAM Users
- to collect data on all the IAM Users in your AWS account, run the `iam/list-iam-users.py` script to generate a file called `iam/users.json`
- `iam/users.json` will contain a dictionary with each key being the `username`, and each value being the `policy arns` for each attached iam policy.
- After the `iam/users.json` file has been created, run the`iam/list-user-perms.py`. This will create a file for each iam user (filename = username). Inside each file will contain the json policy for each iam policy that is attached to that user. Each file will be placed inside the `iam/users/` directory.

### IAM Roles
- to collect data on all the IAM roles in your AWS account, run the `iam/list-iam-roles.py` script to generate a file called `iam/roles.json`
- `iam/roles.json` will contain a dictionary with each key being the `role name`, and each value being the `policy arns` for each attached iam policy.
- After the `iam/roles.json` file has been created, run the`iam/list-role-perms.py`. This will create a file for each iam role (filename = role name). Inside each file will contain the json policy for each iam policy that is attached to that role. Each file will be placed inside the `iam/roles/` directory.

### KMS Keys
- To collect data on all the KMS Customer Managed Keys in your AWS account, run the `kms/list-kms-keys.py` script to generate a file for each Customer Managed Key (filename = key alias). Inside each file will contain the json key policy. Each file will be placed inside the `kms/keys/` directory.
