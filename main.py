from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="WUN (What You Need) - Intent Router",
    version="1.0.0",
    description="Middleware di Intent-Routing sicuro e senza memorizzazione di dati sensibili."
)

class SearchRequest(BaseModel):
    category: str = Field(..., description="Macro-categoria (es. Tech, Abbigliamento, Casa, Altro)")
    custom_query: Optional[str] = Field(None, description="Usato se category è 'Altro'")
    budget: float = Field(..., gt=0, description="Budget massimo inserito dall'utente")
    extra_filter: Optional[str] = Field(None, description="Filtro rapido di dettaglio")
    accepted_disclaimer: bool = Field(..., description="Conferma declinazione responsabilità")
    accepted_privacy: bool = Field(..., description="Conferma privacy zero dati sensibili")

AFFILIATE_TAGS = {
    "amazon_it": "iltuonome-21",
}

@app.post("/api/v1/route", status_code=status.HTTP_200_OK)
def process_intent(data: SearchRequest):
    if not data.accepted_disclaimer or not data.accepted_privacy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Devi accettare le condizioni legali e la privacy per procedere."
        )
    
    search_term = data.custom_query if data.category.lower() == "altro" and data.custom_query else data.category
    if data.extra_filter:
        search_term += f" {data.extra_filter}"
        
    formatted_query = search_term.replace(" ", "+")
    target_url = f"https://www.amazon.it/s?k={formatted_query}&tag={AFFILIATE_TAGS['amazon_it']}"
    
    return {
        "status": "success",
        "intent_processed": search_term,
        "max_budget": data.budget,
        "merchant_target": "Amazon Ufficiale (Accreditato)",
        "redirect_url": target_url,
        "notice": "Il cliente viene reindirizzato in autonomia. WUN non gestisce pagamenti o dati personali."
    }

@app.get("/")
def health_check():
    return {"status": "WUN Engine is online and ready.", "mode": "Middleware Intent-Routing"}