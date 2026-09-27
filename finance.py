from typing import List, Optional
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
  return [
      PartnerLink(
          partner_name="Facile.it",
          description="Confronto preventivo assicurazioni, mutui e tariffe",
          url="https://www.facile.it/",
      ),
      PartnerLink(
          partner_name="Segugio.it",
          description="Risparmia su assicurazione auto, moto e prestiti",
          url="https://www.segugio.it/",
      ),
      PartnerLink(
          partner_name="MutuiOnline.it",
          description="Il comparatore n.1 in Italia per i mutui casa",
          url="https://www.mutuionline.it/",
      ),
  ]