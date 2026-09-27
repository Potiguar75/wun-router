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
  query = urllib.parse.quote(custom_query or "sport hobby")
  budget_int = int(budget)
  return [
      PartnerLink(
          partner_name="Decathlon",
          description=(
              f"Attrezzatura sportiva e hobby per '{custom_query or 'sport'}'"
          ),
          url=f"https://www.decathlon.it/search?Ntt={query}",
      ),
      PartnerLink(
          partner_name="Amazon IT (Sport & Hobby)",
          description="Tutto per il tempo libero e passioni",
          url=(
              f"https://www.amazon.it/s?k={query}&rh=p_36%3A-{budget_int * 100}&tag=wun03-21"
          ),
      ),
      PartnerLink(
          partner_name="eBay",
          description="Collezionismo, giochi e articoli sportivi",
          url=(
              f"https://www.ebay.it/sch/i.html?_nkw={query}&_udmax={budget_int}"
          ),
      ),
  ]