from zenml.steps import step
import pandas as pd
from zenml.integrations.pandas.materializers import PandasMaterializer
from typing import Annotated

@step
def load_data() -> pd.DataFrame:
    df = pd.read_csv("./data/uber.csv")
    return df