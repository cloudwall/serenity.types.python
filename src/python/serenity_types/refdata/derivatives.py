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


class DerivativeAsset(Asset):
    """
    A listed or OTC derivative contract.
    """

    underlier_exposure_id: UUID
    """
    The underlying exposure that this derivatives references, e.g. BTC (tok.btc).
    """

    reference_index_id: Optional[UUID]
    """
    The specific index, e.g. Deribit BTC Index, used to get a fair price for the underlying at settlement time.
    """

    contract_size: float
    """
    Size of the contract in qty of underlying.
    """

    settlement_exposure_id: UUID
    """
    The exposure that this derivatives settles in, e.g. on Deribit, CASH settled, it might be USD.
    """

    settlement_type: SettlementType
    """
    Whether this contract settles in cash or in the underlying itself.
    """


class ListedDerivative(DerivativeAsset):
    """
    An exchange-listed derivative contract.
    """

    exchange_id: UUID
    """
    The exchange on which this contract is listed.
    """


class Expiry(CamelModel):
    expiration_date: date

    expiration_time: time
