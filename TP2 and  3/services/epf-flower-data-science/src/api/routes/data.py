from fastapi import APIRouter
import requests
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import kagglehub

router = APIRouter()

@router.get("/download-dataset")
def download_csv(destination="src/data"):
    """
    Downloads the Iris dataset using kagglehub and saves it to the specified destination.
    """
    try:
        # Ensure the destination folder exists
        os.makedirs(destination, exist_ok=True)
        
        # Download the dataset
        print("Downloading the Iris dataset...")
        path = kagglehub.dataset_download("uciml/iris")
        
        # Move the dataset files to the destination directory
        if path:
            files = os.listdir(path)
            for file in files:
                full_file_path = os.path.join(path, file)
                if os.path.isfile(full_file_path):
                    os.rename(full_file_path, os.path.join(destination, file))
            
            print(f"Dataset downloaded and moved to {destination}")
        else:
            print("Failed to download dataset. Check kagglehub installation or dataset URL.")

    except Exception as e:
        print(f"An error occurred while downloading the dataset: {e}")

@router.get("/load-dataset")
def load_dataset():
    """
    Loads the Iris dataset from the saved file and returns it as a JSON response.
    """
    filepath = "/Users/samwall/Documents/5A/Samuel_WALL_API---Webscrapping/TP2 and  3/services/epf-flower-data-science/src/data/iris.csv"
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