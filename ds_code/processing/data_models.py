from pydantic import BaseModel, Field
from typing import Optional

class Imovel(BaseModel):
    id: str = Field(..., alias='_id')
    lat: Optional[float] = None
    lon: Optional[float] = None
    usable_areas: Optional[int] = None
    parking_spaces: Optional[int] = None
    suites: Optional[int] = None
    bathrooms: Optional[int] = None
    total_areas: Optional[int] = None
    bedrooms: Optional[int] = None
    geohash: Optional[str] = None
    price: Optional[int] = None
    yearly_iptu: Optional[int] = None
    monthly_condo_fee: Optional[int] = None
    has_gym: bool
    has_garden: bool
    has_pool: bool
    has_lobby: bool
    has_party_room: bool
    has_balcony: bool
    has_playground: bool
    has_grill: bool
    has_games: bool
    has_closet: bool
    has_elevator: bool
    has_furnitures: bool
    has_toilet: bool
    has_massage_room: bool
    has_washhouse: bool
    has_terrace: bool
    has_pilates: bool
    has_fancy_words: bool
    has_shield: bool
    has_drivers_room: bool
    has_biometry: bool
    has_fireplace: bool
    has_deposit: bool
    has_ceiling_height: bool
    has_generator: bool
    has_pantry: bool
    is_duplex: bool
    is_triplex: bool
    total_dom_part_improvisados: Optional[int] = None
    renda_nom_dom_part: Optional[int] = None
    renda_nom_dom_part_perm: Optional[int] = None
    renda_nom_dom_part_imp: Optional[int] = None
    renda_nom_dom_sal_baixo1: Optional[int] = None
    renda_nom_dom_sal_baixo2: Optional[int] = None
    renda_nom_dom_sal_baixo3: Optional[int] = None
    renda_nom_dom_sal_baixo4: Optional[int] = None
    renda_nom_dom_sal_medio1: Optional[int] = None
    renda_nom_dom_sal_medio2: Optional[int] = None
    renda_nom_dom_sal_medio3: Optional[int] = None
    renda_nom_dom_sal_alto1: Optional[int] = None
    renda_nom_dom_sal_alto2: Optional[int] = None
    renda_nom_dom_sem_rendimento: Optional[int] = None
    ident_logradouro_proprios: Optional[int] = None
    nao_ident_logradouro_proprios: Optional[int] = None
    ident_logradouro_alugados: Optional[int] = None
    nao_ident_logradouro_alugados: Optional[int] = None
    ilum_publica_proprios: Optional[int] = None
    nao_ilum_publica_proprios: Optional[int] = None
    ilum_publica_alugados: Optional[int] = None
    nao_ilum_publica_alugados: Optional[int] = None