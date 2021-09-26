from azureml.core import Environment, Workspace
from azureml.core.model import InferenceConfig, Model
from azureml.core.webservice import AciWebservice

aciconfig = AciWebservice.deploy_configuration(cpu_cores=2,
                                               memory_gb=4,
                                               tags={"data": "roberta-base"},
                                               description='Predict Robertabase')
ws = Workspace.from_config()
model = Model(ws, 'roberta-base')
curated_env_name = 'AzureML-PyTorch-1.6-GPU'
# pytorch_env = Environment.get(workspace=ws, name=curated_env_name)
pytorch_env = Environment.from_conda_specification(name='pytorch-1.6-gpu', file_path='./model/conda_dependencies.yml')
# pytorch_env.save_to_directory(path=curated_env_name)

#env = Environment(name="project_environment")
dummy_inference_config = InferenceConfig(
    environment=pytorch_env,
    # source_directory="./source_dir",
    entry_script="./model/entry_script.py",
)

service = Model.deploy(
    ws,
    "myservice",
    [model],
    dummy_inference_config,
    deployment_config=aciconfig,
    overwrite=True,
)
service.wait_for_deployment(show_output=True)
print(service.get_logs())
print(service.scoring_uri)
