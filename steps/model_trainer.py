# from zenml.steps import step
# import pandas as pd
# import pickle
# from sklearn.linear_model import LinearRegression
# import pandas as pd

# @step
# def train_model(X_train: pd.DataFrame, y_train: pd.Series):
    
#     # X = df.drop("fare_amount", axis=1)
#     # y = df["fare_amount"]
#     # print(X)
#     X = X_train
#     y = y_train
#     model = LinearRegression()
#     model.fit(X, y)
#     with open("./models/model.pkl", "wb") as f:
#         pickle.dump(model, f)

#     return model

from zenml.steps import step
import pandas as pd
import pickle
import xgboost as xgb
import os

@step
def train_model(X_train: pd.DataFrame, y_train: pd.Series):
    """
    Train XGBoost model without validation
    """
    os.makedirs("./models", exist_ok=True)
    
    # Initialize XGBoost Regressor
    model = xgb.XGBRegressor(
        n_estimators=100,           # Number of trees
        learning_rate=0.1,          # Learning rate
        max_depth=6,                # Maximum depth of trees
        min_child_weight=1,
        subsample=0.8,
        colsample_bytree=0.8,
        gamma=0,
        reg_alpha=0.1,              # L1 regularization
        reg_lambda=1,               # L2 regularization
        random_state=42,
        n_jobs=-1,
        verbosity=1
    )

    
    # Fit the model
    model.fit(X_train, y_train)
    
    # Save the model
    with open("./models/model.pkl", "wb") as f:
        pickle.dump(model, f)
    

    
    return model