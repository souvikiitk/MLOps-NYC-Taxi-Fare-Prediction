# from zenml.client import Client
# import pickle

# artifact_uri = Client().get_pipeline('fare_prediction_pipeline').runs[-1].steps("train_model").output.uri
# model_path = f"{artifact_uri}/model.pkl"

# with open(model_path, 'rb') as file:
#     model = pickle.load(file)


from zenml.client import Client
import pickle

client = Client()

# Get the latest pipeline run
pipeline = client.get_pipeline('fare_prediction_pipeline')
latest_run = pipeline.runs[-1]

# Access the step using the steps property
train_model_step = latest_run.steps["train_model"]

# Get the output artifact URI
artifact_uri = train_model_step.output.uri
model_path = f"{artifact_uri}/model.pkl"

# Load the model
with open("models/model.pkl", 'rb') as file:
    model = pickle.load(file)