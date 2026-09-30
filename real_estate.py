from typing import Dict, List, Optional
import urllib.parse


def get_partners(
    budget: float,
    sub_type: Optional[str] = None,
    location: Optional[str] = None,
    custom_query: Optional[str] = None,
) -> List[Dict[str, str]]:
  loc_raw = (location or "italia").strip().lower()
  loc_slug = loc_raw.replace(" ", "-")
  tipo = sub_type or "vendita"
  budget_int = int(budget)

  imm_url = f"https://www.immobiliare.it/{'vendita' if tipo=='vendita' else 'affitto'}-case/{loc_slug}/?prezzoMassimo={budget_int}"
  idealista_loc = f"{loc_slug}-{loc_slug}"
  idealista_url = f"https://www.idealista.it/{'affitto' if tipo=='affitto' else 'vendita'}-case/{idealista_loc}/con-prezzo_{budget_int}/"
  casa_url = f"https://www.casa.it/{'vendita' if tipo=='vendita' else 'affitto'}/residenziale/{loc_slug}/?prezzoMax={budget_int}"

  return [
      {
          "partner_name": "Immobiliare.it",
          "description": f"Ricerca mirata ({tipo}) a {location or 'Italia'}",
          "url": imm_url,
      },
      {
          "partner_name": "Idealista",
          "description": f"Annunci verificati di case in {tipo}",
          "url": idealista_url,
      },
      {
          "partner_name": "Casa.it",
          "description": (
              f"Network nazionale immobiliare per {location or 'Italia'}"
          ),
          "url": casa_url,
      },
  ]

