from zenml.pipelines import pipeline
from steps.data_loader import load_data
from steps.feature_engineer import feature_engineering
from steps.model_trainer import train_model
from steps.model_evaluator import model_evaluator_step

@pipeline
def fare_prediction_pipeline():
    df = load_data()
    # features = feature_engineering(df)
    X_train, X_test, y_train, y_test = feature_engineering(df)
    model = train_model(X_train, y_train)
    model_evaluator_step(model, X_test,y_test)