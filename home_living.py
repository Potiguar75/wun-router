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
  query = urllib.parse.quote(custom_query or "arredamento casa")
  budget_int = int(budget)
  return [
      PartnerLink(
          partner_name="IKEA Italia",
          description=(
              f"Mobili e soluzioni d'arredo per '{custom_query or 'casa'}'"
          ),
          url=f"https://www.ikea.com/it/it/search/?q={query}",
      ),
      PartnerLink(
          partner_name="Leroy Merlin",
          description="Fai da te, giardino, bagno e ristrutturazione",
          url=f"https://www.leroymerlin.it/search?q={query}",
      ),
      PartnerLink(
          partner_name="Amazon IT (Casa)",
          description="Complementi d'arredo e oggetti per la casa",
          url=(
              f"https://www.amazon.it/s?k={query}&rh=p_36%3A-{budget_int * 100}&tag=wun03-21"
          ),
      ),
  ]