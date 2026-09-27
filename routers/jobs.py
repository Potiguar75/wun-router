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
  q = urllib.parse.quote(custom_query or "lavoro")
  loc = urllib.parse.quote(location or "italia")
  return [
      PartnerLink(
          partner_name="Indeed",
          description=f"Offerte di lavoro per '{custom_query or 'impiego'}'",
          url=f"https://it.indeed.com/jobs?q={q}&l={loc}",
      ),
      PartnerLink(
          partner_name="LinkedIn Jobs",
          description="Opportunità professionali e networking",
          url=(
              f"https://www.linkedin.com/jobs/search/?keywords={q}&location={loc}"
          ),
      ),
      PartnerLink(
          partner_name="InfoJobs",
          description="Annunci di lavoro e candidature rapide",
          url=f"https://www.infojobs.it/offerte-lavoro?keyword={q}",
      ),
  ]