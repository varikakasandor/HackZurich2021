from azureml.core import Workspace
from azureml.core.model import Model

import json
config_path = '.azureml/config.json'
with open(config_path) as json_file:
    data = json.load(json_file)
SUBSCRIPTION_ID = 'subscription_id'
RESOURCE_GROUP = 'resource_group'
WORKSPACE_NAME = 'workspace_name'
subscription_id = data[SUBSCRIPTION_ID]
resource_group = data[RESOURCE_GROUP]
workspace_name = data[WORKSPACE_NAME]
# TODO: hardcoded path for now
model_path = '/Users/marcinbodych/Workspace/hackzurich/data/roberta-base/pytorch_model.bin'
ws = Workspace.from_config()
print('Registering the model...')
model = Model.register(ws, model_name="roberta-base", model_path=model_path)
