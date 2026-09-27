from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import corretto dei moduli dalla cartella router
from router import (
    automotive,
    fashion,
    finance,
    general,
    hobby,
    home_living,
    jobs,
    real_estate,
    tech,
    travel,
)

app = FastAPI(title="WUN Universal Intent Router", version="3.0")

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
  sub_type: Optional[str] = None
  location: Optional[str] = None
  custom_query: Optional[str] = None
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
    raise HTTPException(
        status_code=400,
        detail=(
            "È necessario accettare i termini di orientamento e la privacy."
        ),
    )

  cat_lower = req.category.lower()
  partners = []

  if "casa & immobili" in cat_lower:
    partners = real_estate.get_partners(
        req.budget, req.sub_type, req.location, req.custom_query
    )
  elif "arredamento" in cat_lower:
    partners = home_living.get_partners(
        req.budget, req.sub_type, req.location, req.custom_query
    )
  elif "abbigliamento" in cat_lower:
    partners = fashion.get_partners(
        req.budget, req.sub_type, req.location, req.custom_query
    )
  elif "hobby" in cat_lower:
    partners = hobby.get_partners(
        req.budget, req.sub_type, req.location, req.custom_query
    )
  elif "auto" in cat_lower or "moto" in cat_lower:
    partners = automotive.get_partners(
        req.budget, req.sub_type, req.location, req.custom_query
    )
  elif "viaggi" in cat_lower or "hotel" in cat_lower:
    partners = travel.get_partners(
        req.budget, req.sub_type, req.location, req.custom_query
    )
  elif "tech" in cat_lower or "elettronica" in cat_lower:
    partners = tech.get_partners(
        req.budget, req.sub_type, req.location, req.custom_query
    )
  elif "finanza" in cat_lower or "assicurazioni" in cat_lower:
    partners = finance.get_partners(
        req.budget, req.sub_type, req.location, req.custom_query
    )
  elif "lavoro" in cat_lower or "formazione" in cat_lower:
    partners = jobs.get_partners(
        req.budget, req.sub_type, req.location, req.custom_query
    )
  else:
    partners = general.get_partners(
        req.budget, req.sub_type, req.location, req.custom_query
    )

  return RouteResponse(
      status="success",
      category=req.category,
      summary_intent=f"Ricerca per {req.category} (Budget max: {req.budget}€)",
      partners=partners,
  )


@app.get("/")
def health_check():
  return {"status": "WUN Router is online", "version": "3.0"}