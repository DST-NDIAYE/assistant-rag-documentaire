from fastapi import FastAPI
from app.rag_pipeline import AssistantDocumentaire


import os 
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")
app = FastAPI()

assistant = AssistantDocumentaire(api_key)
assistant.charger_document("documents")

from pydantic import BaseModel
class QuestionRequest(BaseModel):
    question: str




@app.get("/")
def accueil():
    return {
        "message": "API opérationnelle "
    }

@app.post("/question")
def poser_question_api(requete: QuestionRequest):
    resultat = assistant.poser_question(
        requete.question
    )

    return resultat