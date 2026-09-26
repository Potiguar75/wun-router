from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="WUN (What You Need) - Intent Router",
    version="1.0.0",
    description="Middleware di Intent-Routing sicuro e senza memorizzazione di dati sensibili."
)

# Configurazione CORS per permettere al widget frontend di comunicare senza blocchi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    category: str
    custom_query: Optional[str] = None
    budget: float
    extra_filter: Optional[str] = None
    accepted_disclaimer: bool
    accepted_privacy: bool

@app.get("/")
def health_check():
    return {"status": "WUN Engine is online and ready.", "mode": "Middleware Intent-Routing"}

@app.post("/api/v1/route")
def process_intent(payload: SearchRequest):
    # Controllo di sicurezza rigoroso sulle spunte legali obbligatorie
    if not payload.accepted_disclaimer or not payload.accepted_privacy:
        raise HTTPException(
            status_code=400,
            detail="Accesso negato: è obbligatorio accettare il disclaimer e la privacy policy per la protezione dei dati."
        )
    
    # Determina la query di ricerca finale
    query_term = payload.custom_query if payload.category.lower() == "altro" and payload.custom_query else payload.category
    if payload.extra_filter:
        query_term = f"{query_term} {payload.extra_filter}"
    
    # Formattazione per la ricerca sul merchant partner
    formatted_query = query_term.replace(" ", "+")
    redirect_url = f"https://www.amazon.it/s?k={formatted_query}&tag=iltuonome-21"
    
    return {
        "status": "success",
        "intent_processed": query_term,
        "merchant_target": "Amazon Ufficiale (Accreditato)",
        "redirect_url": redirect_url,
        "notice": "Il cliente viene reindirizzato in autonomia. WUN non gestisce pagamenti o dati personali."
    }