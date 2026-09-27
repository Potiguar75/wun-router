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
  query = urllib.parse.quote(custom_query or "elettronica tech")
  budget_int = int(budget)
  return [
      PartnerLink(
          partner_name="Amazon IT",
          description="Spedizione rapida e garanzia Prime",
          url=(
              f"https://www.amazon.it/s?k={query}&rh=p_36%3A-{budget_int * 100}&tag=wun03-21"
          ),
      ),
      PartnerLink(
          partner_name="Trovaprezzi.it",
          description="Comparatore prezzi ufficiale e negozi certificati",
          url=(
              f"https://www.trovaprezzi.it/prezzo_prodotti-chiave.aspx?q={query}&prezzomax={budget_int}"
          ),
      ),
      PartnerLink(
          partner_name="MediaWorld",
          description="Offerte e tecnologia di marca",
          url=f"https://www.mediaworld.it/it/search.html?keyword={query}",
      ),
  ]