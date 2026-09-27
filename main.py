from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import urllib.parse

app = FastAPI(title="WUN Universal Smart Intent Router", version="2.0")

# Abilitiamo il CORS per permettere le chiamate dal frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione puoi restringere al dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RouteRequest(BaseModel):
    category: str
    budget: float
    # Campi dinamici per le categorie avanzate
    sub_type: Optional[str] = None      # Es. Affitto/Vendita per case, Hotel/Volo per viaggi
    location: Optional[str] = None      # Località o destinazione
    custom_query: Optional[str] = None  # Specifiche libere o modello
    extra_filter: Optional[str] = None  # Filtri rapidi opzionali
    accepted_disclaimer: bool
    accepted_privacy: bool

@app.post("/api/v1/route")
async def route_intent(req: RouteRequest):
    if not req.accepted_disclaimer or not req.accepted_privacy:
        raise HTTPException(status_code=400, detail="È necessario accettare i termini di orientamento e privacy.")

    category_lower = req.category.lower()
    
    # Dizionario o logica di mappatura per i diversi verticali
    target_merchant = "Generale"
    redirect_url = "https://www.google.com"

    # 1. CATEGORIA: IMMOBILI / CASE
    if "casa" in category_lower or "immobili" in category_lower:
        target_merchant = "Portale Immobiliare Partner"
        loc = urllib.parse.quote(req.location or "Italia")
        tipo = urllib.parse.quote(req.sub_type or "vendita")
        # Esempio di generazione link di ricerca mirata
        redirect_url = f"https://www.immobiliare.it/vendita-case/{loc}/?maxPrice={req.budget}"
        if "affitto" in req.sub_type.lower():
            redirect_url = f"https://www.immobiliare.it/affitto-case/{loc}/?maxPrice={req.budget}"

    # 2. CATEGORIA: AUTOMOTIVE / AUTO & MOTO
    elif "auto" in category_lower or "moto" in category_lower:
        target_merchant = "Portale Automotive Partner"
        query = urllib.parse.quote(req.custom_query or req.category)
        redirect_url = f"https://www.autoscout24.it/lst/{query}?priceto={req.budget}"

    # 3. CATEGORIA: VIAGGI & HOTEL / ALBERGHI
    elif "viaggi" in category_lower or "hotel" in category_lower or "alberghi" in category_lower:
        target_merchant = "Booking & Travel Partner"
        dest = urllib.parse.quote(req.location or "Europa")
        redirect_url = f"https://www.booking.com/searchresults.html?ss={dest}&budget={req.budget}"

    # 4. CATEGORIA: TECH & ELETTRONICA (E-commerce)
    elif "tech" in category_lower or "elettronica" in category_lower:
        target_merchant = "Amazon Associates / Tech Partner"
        query = urllib.parse.quote(req.custom_query or "smartphone pc")
        # Inserisci qui il tuo tag di affiliazione reale (es. &tag=tuotag-21)
        redirect_url = f"https://www.amazon.it/s?k={query}&rh=p_36%3A-{int(req.budget * 100)}&tag=wun03-21"

    # 5. CATEGORIA: ALTRO / GENERALE (Fallback universale)
    else:
        target_merchant = "Network Partner Multi-Categoria"
        query = urllib.parse.quote(req.custom_query or req.category)
        redirect_url = f"https://www.trovaprezzi.it/prezzo_prodotti-chiave.aspx?q={query}"

    return {
        "status": "success",
        "category": req.category,
        "merchant_target": target_merchant,
        "redirect_url": redirect_url,
        "privacy_verified": True
    }

@app.get("/")
def health_check():
    return {"status": "WUN Universal Router is online", "version": "2.0"}