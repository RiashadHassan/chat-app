from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health_check():
    return {"Status": "Welcome to the Chat Service!"}
