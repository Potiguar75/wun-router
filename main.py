from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import urllib.parse

app = FastAPI(title="WUN Universal Multi-Partner Router", version="2.3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RouteRequest(BaseModel):
    category: str
    budget: float
    sub_type: Optional[str] = None      # Affitto / Vendita
    location: Optional[str] = None      # Località o Città
    custom_query: Optional[str] = None  # Specifiche libere
    accepted_disclaimer: bool
    accepted_privacy: bool

class PartnerLink(BaseModel):
    partner_name: str
    description: str
    url: str

class RouteResponse(BaseModel):
    status: str
    category: str
    summary_intent: str
    partners: List[PartnerLink]

@app.post("/api/v1/route", response_model=RouteResponse)
async def route_intent(req: RouteRequest):
    if not req.accepted_disclaimer or not req.accepted_privacy:
        raise HTTPException(status_code=400, detail="È necessario accettare i termini di orientamento e privacy.")

    category_lower = req.category.lower()
    partners = []

    # 1. IMMOBILI / CASE
    if "casa" in category_lower or "immobili" in category_lower:
        loc_raw = (req.location or "italia").strip().lower()
        loc_slug = loc_raw.replace(" ", "-")
        tipo = req.sub_type or "vendita"
        
        # URL corretto per Immobiliare.it (es. /affitto-case/trento/ o /vendita-case/trento/)
        imm_url = f"https://www.immobiliare.it/{'vendita' if tipo=='vendita' else 'affitto'}-case/{loc_slug}/?prezzoMassimo={int(req.budget)}"
        
        # URL corretto per Idealista (es. /affitto-case/trento-trento/con-prezzo_max_.../)
        idealista_loc = f"{loc_slug}-{loc_slug}"
        idealista_url = f"https://www.idealista.it/{'affitto' if tipo=='affitto' else 'vendita'}-case/{idealista_loc}/con-prezzo_max_{int(req.budget)}/"
        
        # Casa.it (lasciato intatto come da tua richiesta)
        casa_url = f"https://www.casa.it/{'vendita' if tipo=='vendita' else 'affitto'}/residenziale/{loc_slug}/?prezzoMax={int(req.budget)}"

        partners = [
            PartnerLink(
                partner_name="Immobiliare.it",
                description=f"Ricerca mirata ({tipo}) a {req.location} entro i {req.budget}€",
                url=imm_url
            ),
            PartnerLink(
                partner_name="Idealista",
                description=f"Annunci verificati di case in {tipo} nella zona",
                url=idealista_url
            ),
            PartnerLink(
                partner_name="Casa.it",
                description=f"Network nazionale immobiliare per {req.location}",
                url=casa_url
            )
        ]

    # 2. AUTO & MOTO
    elif "auto" in category_lower or "moto" in category_lower:
        query = urllib.parse.quote(req.custom_query or req.category)
        partners = [
            PartnerLink(
                partner_name="AutoScout24",
                description=f"Il marketplace europeo n.1 per {req.custom_query}",
                url=f"https://www.autoscout24.it/lst/{query}?priceto={int(req.budget)}"
            ),
            PartnerLink(
                partner_name="Subito.it",
                description="Annunci diretti da privati e concessionari",
                url=f"https://www.subito.it/annunci-italia/vendita/usato/?q={query}&ps={int(req.budget)}"
            ),
            PartnerLink(
                partner_name="Autohero",
                description="Auto ricondizionate con garanzia e consegna a domicilio",
                url=f"https://www.autohero.com/it/search/?priceMax={int(req.budget)}"
            )
        ]

    # 3. VIAGGI & HOTEL
    elif "viaggi" in category_lower or "hotel" in category_lower:
        dest = urllib.parse.quote(req.location or "Europa")
        partners = [
            PartnerLink(
                partner_name="Booking.com",
                description=f"Migliori tariffe alberghiere a {req.location}",
                url=f"https://www.booking.com/searchresults.html?ss={dest}&price_max=val_{int(req.budget)}"
            ),
            PartnerLink(
                partner_name="Expedia",
                description="Offerte pacchetti volo + hotel",
                url=f"https://www.expedia.it/Abitazioni-{dest}.d602055.Guida-Viaggi?maxPrice={int(req.budget)}"
            ),
            PartnerLink(
                partner_name="Airbnb",
                description=f"Case vacanza uniche a {req.location}",
                url=f"https://www.airbnb.it/s/{dest}/homes?price_max={int(req.budget)}"
            )
        ]

    # 4. TECH & ELETTRONICA
    elif "tech" in category_lower or "elettronica" in category_lower:
        query = urllib.parse.quote(req.custom_query or "elettronica")
        partners = [
            PartnerLink(
                partner_name="Amazon IT",
                description="Spedizione rapida e garanzia Prime",
                url=f"https://www.amazon.it/s?k={query}&rh=p_36%3A-{int(req.budget * 100)}&tag=wun03-21"
            ),
            PartnerLink(
                partner_name="Trovaprezzi.it",
                description="Comparatore prezzi ufficiale e negozi certificati",
                url=f"https://www.trovaprezzi.it/prezzo_prodotti-chiave.aspx?q={query}&prezzomax={int(req.budget)}"
            ),
            PartnerLink(
                partner_name="eBay",
                description="Offerte e aste tech imperdibili",
                url=f"https://www.ebay.it/sch/i.html?_nkw={query}&_udmax={int(req.budget)}"
            )
        ]

    # 5. ALTRO / GENERALE
    else:
        query = urllib.parse.quote(req.custom_query or req.category)
        partners = [
            PartnerLink(
                partner_name="Trovaprezzi Universale",
                description="Motore di ricerca prezzi multi-categoria",
                url=f"https://www.trovaprezzi.it/prezzo_prodotti-chiave.aspx?q={query}&prezzomax={int(req.budget)}"
            ),
            PartnerLink(
                partner_name="Google Shopping",
                description="Esplora tutte le opzioni di mercato",
                url=f"https://www.google.com/search?q={query}+max+{int(req.budget)}&tbm=shop"
            )
        ]

    return RouteResponse(
        status="success",
        category=req.category,
        summary_intent=f"Ricerca per {req.category} (Budget max: {req.budget}€)",
        partners=partners
    )

@app.get("/")
def health_check():
    return {"status": "WUN Multi-Partner Router is online", "version": "2.3"}