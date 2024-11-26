import uvicorn
from fastapi.responses import RedirectResponse
from src.app import get_application

app = get_application()

@app.get("/", include_in_schema=False)  # Root route that won't appear in Swagger docs
def redirect_to_docs():
    """
    Redirects the root URL to the Swagger documentation.
    """
    return RedirectResponse(url="/docs")  # Redirects to Swagger UI

if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True, port=8080)
