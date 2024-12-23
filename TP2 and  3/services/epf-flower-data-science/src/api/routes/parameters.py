from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.firestore import FirestoreClient

router = APIRouter()

firestore_client = FirestoreClient()

class UpdateParametersInput(BaseModel):
    n_estimators: int
    criterion: str

@router.get("/create-firestore-collection")
def create_firestore_collection():
    """
    Creates the Firestore collection "parameters" with the specified parameters.
    """
    try:
        
        parameters = {
            "n_estimators": 100,
            "criterion": "gini"
        }
        
        firestore_client.set("parameters", "parameters", parameters)
        
        return {"message": "Firestore collection and document created successfully."}
    except Exception as e:
        return {"error": f"An error occurred while creating the Firestore collection: {str(e)}"}


@router.get("/retrieve-parameters")
def retrieve_parameters():
    """
    Retrieves the parameters from the Firestore collection.
    """
    try:
        parameters = firestore_client.get("parameters", "parameters")
        return {"parameters": parameters}
    except FileNotFoundError:
        return {"error": "Parameters not found in Firestore."}
    except Exception as e:
        return {"error": f"An error occurred while retrieving the parameters: {str(e)}"}
    


@router.post("/update-parameters")
def update_parameters(input_data: UpdateParametersInput):
    """
    Updates the parameters in the Firestore collection.
    """
    try:
        parameters = {
            "n_estimators": input_data.n_estimators,
            "criterion": input_data.criterion
        }
        firestore_client.set("parameters", "parameters", parameters)
        return {"message": "Parameters updated successfully."}
    except Exception as e:
        return {"error": f"An error occurred while updating the parameters: {str(e)}"}