from zenml.steps import step
from zenml.client import Client
from sklearn.metrics import accuracy_score
from zenml.experiment_trackers import BaseExperimentTracker   
from sklearn.metrics import mean_absolute_error
import pickle
import pandas as pd

@step
def model_evaluator_step(model, X_test: pd.DataFrame, y_test: pd.Series) -> float:
     
    # with open(model_path, "rb") as f:
    #     model = pickle.load(f)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    # predictions = model.predict(X_test)
    # accuracy = accuracy_score(y_test, predictions)
    print(f"Model accuracy: {mae:.2f}")

    # Log to experiment tracker (e.g., MLflow)
    tracker = Client().active_stack.experiment_tracker
    if tracker:
        tracker.log_metric("accuracy", mae)

    return mae