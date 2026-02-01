from fastapi import FastAPI, Body
from ollama import Client
app = FastAPI()
client=Client(
    host="http://localhost:11434",
)
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/contact")
def read_contact():
    return {"email": "contact@example.com"}

@app.post("/chat")
def chat(message: str=Body(..., description="The Message")):
    res=client.chat(
        model="gemma:2b",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return {"response": res.message.content}