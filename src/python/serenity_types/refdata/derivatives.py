from datetime import date, time
from enum import Enum
from typing import Optional
from uuid import UUID

from serenity_types.refdata.asset import Asset
from serenity_types.utils.serialization import CamelModel


class SettlementType(Enum):
    CASH = 'CASH'
    """
    Derivative contract settled in fiat or stablecoins.
    """

    PHYSICAL = 'PHYSICAL'
    """
    Derivative contract settled in an asset other than fiat or stablecoins.
    """


class PayoffType(Enum):
    LINEAR = 'LINEAR'
    """
    Linear payoff that follows the price movement of the underlier.
    """

    INVERSE = 'INVERSE'
    """
    Non-linear payoff that moves opposite the underlying price movements.
    """


class ListedDerivative(Asset):
    """
    An exchange-listed derivative contract.
    """
    exchange_symbol: str

    underlier_exposure_id: UUID

    reference_exposure_id: Optional[UUID]

    quote_exposure_id: UUID

    exchange_id: UUID

    contract_size: float

    settlement_type: SettlementType


class Expiry(CamelModel):
    expiration_date: date

    expiration_time: time
