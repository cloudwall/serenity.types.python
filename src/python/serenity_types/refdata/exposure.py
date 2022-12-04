from enum import Enum
from typing import Optional
from uuid import UUID

from serenity_types.utils.serialization import CamelModel


class ExposureType(Enum):
    COUNTERPARTY = 'COUNTERPARTY'
    """
    Bilateral exposure to a particular counterparty.
    """

    TOKEN_ISSUER = 'TOKEN_ISSUER'
    """
    Exposure to an issuance of a token.
    """

    DEBT_ISSUER = 'DEBT_ISSUER'
    """
    Exposure to an issuance of debt by a sovereign or corporate entity/
    """

    EQUITY_ISSUER = 'EQUITY_ISSUER'
    """
    Exposure to an issuance of equity by a corporate entity, whether public or private.
    """

    FIAT_ISSUER = 'FIAT_ISSUER'
    """
    Exposure to a sovereign, supranational central bank (ECB) or multinational
    organization (the IMF, for SDR).
    """


class Exposure(CamelModel):
    exposure_id: UUID
    """
    Unique identifier for this exposure.
    """

    exposure_type: ExposureType
    """
    Category of exposure.
    """

    party_org_id: Optional[UUID]
    """
    Where relevant, the legal entity / party that creates this particular
    exposure, e.g the token issuer (e.g. Circle, MakerDAO), or in the case of a counterparty
    exposure to an OTC desk, the DEALER (e.g. Galaxy Digital). In the case of
    a fiat currency exposure, the party is the soverign or, in the case of EUR, the ECB.
    """

    symbol: str
    """
    Serenity's unique symbol for this exposure, e.g. tok.usdc or ccy.usd.
    """

    display_name: str
    """
    Human-readable name for this exposure, e.g. Ethereum or U.S. Dollar.
    """

    icon_uri: Optional[str]
    """
    Optional path for loading an icon representing this exposure; typically a URL.
    """
