from fastapi import APIRouter
import requests
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import kagglehub
import joblib
import json
from pydantic import BaseModel
from sklearn.ensemble import RandomForestClassifier

router = APIRouter()
class PredictionInput(BaseModel):
    data: list

@router.get("/download-dataset")
def download_csv(destination="src/data"):
    """
    Downloads the Iris dataset using kagglehub and saves it to the specified destination.
    """
    try:
        os.makedirs(destination, exist_ok=True)
        print("Downloading the Iris dataset...")
        path = kagglehub.dataset_download("uciml/iris")
        if path:
            files = os.listdir(path)
            for file in files:
                full_file_path = os.path.join(path, file)
                if os.path.isfile(full_file_path):
                    os.rename(full_file_path, os.path.join(destination, file))
            print(f"Dataset downloaded and moved to {destination}")
            return {"message": f"Dataset downloaded and moved to {destination}"}
        else:
            print("Failed to download dataset. Check kagglehub installation or dataset URL.")
            return {"error": "Failed to download dataset. Check kagglehub installation or dataset URL."}
    except Exception as e:
        print(f"An error occurred while downloading the dataset: {e}")
        return {"error": f"An error occurred while downloading the dataset: {e}"}

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
        
        processed_filepath = "src/data/processed_iris.csv"
        df.to_csv(processed_filepath, index=False)
        
        return {"processed_data": df.to_dict(orient="records")}
    except FileNotFoundError:
        return {"error": "Dataset not found. Please download it first."}
    except Exception as e:
        return {"error": f"An error occurred while processing the dataset: {str(e)}"}

@router.get("/split-dataset")
def split_dataset():
    """
    Splits the preprocessed Iris dataset into training and testing sets.
    """
    filepath = "src/data/processed_iris.csv"
    try:
        df = pd.read_csv(filepath)
        train, test = train_test_split(df, test_size=0.2, random_state=42)
        
        train.to_csv("src/data/train.csv", index=False)
        test.to_csv("src/data/test.csv", index=False)
        
        return {"message": "Dataset split into train and test sets successfully."}
    except FileNotFoundError:
        return {"error": "Processed dataset not found. Please process the dataset first."}
    except Exception as e:
        return {"error": f"An error occurred while splitting the dataset: {str(e)}"}

@router.get("/train-model")
def train_model():
    """
    Trains a classification model with the processed training dataset and saves the model.
    """
    train_filepath = "src/data/train.csv"
    try:

        df = pd.read_csv(train_filepath)
        X = df.drop("Species", axis=1)
        y = df["Species"]
        
     
        with open("src/config/model_parameters.json", "r") as f:
            params = json.load(f)
        
   
        model = RandomForestClassifier(**params)
        model.fit(X, y)
        
       
        os.makedirs("src/models", exist_ok=True)
        

        joblib.dump(model, "src/models/model.pkl")
        return {"message": "Model trained and saved successfully."}
    except FileNotFoundError:
        return {"error": "Training dataset not found. Please split the dataset first."}
    except Exception as e:
        return {"error": f"An error occurred while training the model: {str(e)}"}
    
# Making predictions with any given data
@router.post("/predict")
def predict(input_data: PredictionInput):
    """
    Makes predictions with the trained model and input data.
    """
    model_filepath = "src/models/model.pkl"
    try:
     
        model = joblib.load(model_filepath)
        
        
        input_df = pd.DataFrame(input_data.data)
     
        if not all(input_df.applymap(lambda x: isinstance(x, (int, float)))):
            raise ValueError("All input data must be numeric.")
        
     
        predictions = model.predict(input_df)
        
       
        return {"predictions": predictions.tolist()}
    except FileNotFoundError:
        return {"error": "Trained model not found. Please train the model first."}
    except ValueError as ve:
        return {"error": f"Invalid input data: {ve}"}
    except Exception as e:
        return {"error": f"An error occurred while making predictions: {str(e)}"}

# Testing the predict on the test data
@router.get("/predict-test-data")
def predict_test_data():
    """
    Makes predictions with the trained model using the test dataset.
    """
    test_filepath = "src/data/test.csv"
    model_filepath = "src/models/model.pkl"
    try:
        
        test_df = pd.read_csv(test_filepath)
        X_test = test_df.drop("Species", axis=1)
        
   
        model = joblib.load(model_filepath)
        
       
        predictions = model.predict(X_test)
        
   
        return {"predictions": predictions.tolist()}
    except FileNotFoundError:
        return {"error": "Test dataset or trained model not found. Please ensure both are available."}
    except Exception as e:
        return {"error": f"An error occurred while making predictions: {str(e)}"}