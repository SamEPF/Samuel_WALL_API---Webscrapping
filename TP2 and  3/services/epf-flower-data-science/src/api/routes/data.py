from fastapi import APIRouter
import requests
import os
import pandas as pd
from sklearn.model_selection import train_test_split

router = APIRouter()

@router.get("/download-dataset")
def download_dataset():
    url = "https://www.kaggle.com/datasets/uciml/iris/download"  # Replace if incorrect
    filepath = "src/data/iris.csv"
    
    response = requests.get(url)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(response.content)
    return {"message": "Dataset downloaded successfully."}

@router.get("/load-dataset")
def load_dataset():
    """
    Loads the Iris dataset from the saved file and returns it as a JSON response.
    """
    filepath = "src/data/iris.csv"
    try:
        df = pd.read_csv(filepath)
        return {"data": df.to_dict(orient="records")}
    except FileNotFoundError:
        return {"error": "Dataset not found. Please download it first."}

@router.get("/process-dataset")
def process_dataset():
    """
    Processes the Iris dataset by encoding categorical variables
    and handling any missing data if applicable.
    """
    filepath = "src/data/iris.csv"
    try:
        df = pd.read_csv(filepath)
        if "species" in df.columns:
            df["species"] = df["species"].astype("category").cat.codes
        return {"processed_data": df.to_dict(orient="records")}
    except FileNotFoundError:
        return {"error": "Dataset not found. Please download it first."}
    except Exception as e:
        return {"error": f"An error occurred while processing the dataset: {str(e)}"}
    
@router.get("/split-dataset")
def split_dataset():
    filepath = "src/data/iris.csv"
    df = pd.read_csv(filepath)
    train, test = train_test_split(df, test_size=0.2, random_state=42)
    return {"train": train.to_dict(orient="records"), "test": test.to_dict(orient="records")}