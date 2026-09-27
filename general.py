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
  query = urllib.parse.quote(custom_query or "prodotti")
  budget_int = int(budget)
  return [
      PartnerLink(
          partner_name="Trovaprezzi Universale",
          description="Motore di ricerca prezzi multi-categoria",
          url=(
              f"https://www.trovaprezzi.it/prezzo_prodotti-chiave.aspx?q={query}&prezzomax={budget_int}"
          ),
      ),
      PartnerLink(
          partner_name="Google Shopping",
          description="Esplora tutte le opzioni di mercato",
          url=(
              f"https://www.google.com/search?q={query}+max+{budget_int}&tbm=shop"
          ),
      ),
      PartnerLink(
          partner_name="eBay",
          description="Offerte e prodotti da tutto il web",
          url=(
              f"https://www.ebay.it/sch/i.html?_nkw={query}&_udmax={budget_int}"
          ),
      ),
  ]