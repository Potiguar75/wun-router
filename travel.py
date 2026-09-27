from typing import List, Optional
import urllib.parse
from pydantic import BaseModel


class PartnerLink(BaseModel):
  partner_name: str
  description: str
  url: str


def get_partners(
    budget: float,
    sub_type: Optional[str] = None,
    location: Optional[str] = None,
    custom_query: Optional[str] = None,
) -> List[PartnerLink]:
  dest = urllib.parse.quote(location or custom_query or "Europa")
  budget_int = int(budget)
  return [
      PartnerLink(
          partner_name="Booking.com",
          description=f"Migliori tariffe alberghiere a {location or 'meta'}",
          url=(
              f"https://www.booking.com/searchresults.html?ss={dest}&price_max=val_{budget_int}"
          ),
      ),
      PartnerLink(
          partner_name="Expedia",
          description="Offerte pacchetti volo + hotel",
          url=(
              f"https://www.expedia.it/Abitazioni-{dest}.d602055.Guida-Viaggi?maxPrice={budget_int}"
          ),
      ),
      PartnerLink(
          partner_name="Airbnb",
          description=f"Case vacanza uniche a {location or 'meta'}",
          url=f"https://www.airbnb.it/s/{dest}/homes?price_max={budget_int}",
      ),
  ]