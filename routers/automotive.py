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
  query = urllib.parse.quote(custom_query or "auto moto")
  budget_int = int(budget)
  return [
      PartnerLink(
          partner_name="AutoScout24",
          description=(
              f"Il marketplace europeo n.1 per '{custom_query or 'auto'}'"
          ),
          url=f"https://www.autoscout24.it/lst/{query}?priceto={budget_int}",
      ),
      PartnerLink(
          partner_name="Subito.it",
          description="Annunci diretti da privati e concessionari",
          url=(
              f"https://www.subito.it/annunci-italia/vendita/usato/?q={query}&ps={budget_int}"
          ),
      ),
      PartnerLink(
          partner_name="Autohero",
          description="Auto ricondizionate con garanzia",
          url=f"https://www.autohero.com/it/search/?priceMax={budget_int}",
      ),
  ]