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
  query = urllib.parse.quote(custom_query or "moda abbigliamento")
  budget_int = int(budget)
  return [
      PartnerLink(
          partner_name="Zalando",
          description=f"Catalogo moda e scarpe per '{custom_query or 'moda'}'",
          url=f"https://www.zalando.it/catalogo/?q={query}",
      ),
      PartnerLink(
          partner_name="Yoox",
          description="Moda firmata e design di tendenza",
          url=f"https://www.yoox.com/it/donna/ricerca?dept=women&text={query}",
      ),
      PartnerLink(
          partner_name="ASOS",
          description="Tendenze e abbigliamento giovane",
          url=(
              f"https://www.asos.com/it/search/?q={query}&currentpricerange=0-{budget_int}"
          ),
      ),
  ]