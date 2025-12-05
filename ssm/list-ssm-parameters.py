import boto3
import jmespath
import json
import os

ssm = boto3.client('ssm')
relative_folder_path = os.path.dirname(__file__)

parameters_dir = os.path.join(relative_folder_path, 'parameter')
if not os.path.exists(parameters_dir):
    os.makedirs(parameters_dir)

def get_parameters():
    paginator = ssm.get_paginator('describe_parameters')
    page_iterator = paginator.paginate(PaginationConfig={'PageSize': 50})
    parameter_names = []
    for page in page_iterator:
        parameter_names = jmespath.search('Parameters[].Name', page) + parameter_names
    return parameter_names

def get_parameter_data(parameters):
    for parameter in parameters:
        print("#"*50)
        parameter_details = ssm.get_parameter(Name=parameter, WithDecryption=True)['Parameter']
        print(f"creating file with for ssm parameter: {parameter}")
        parameter_output_filename = parameters_dir + "/" + parameter + ".json"
        with open(parameter_output_filename, "a") as outfile:
            outfile.write(json.dumps(parameter_details, indent=2, default=str))
        print("#"*50)

if __name__ == "__main__":
    parameters = get_parameters()
    output_filename = os.path.join(relative_folder_path, 'parameters.json')
    with open(output_filename, "a") as outfile:
        outfile.write(json.dumps(parameters, indent=2, default=str))
    get_parameter_data(parameters)

