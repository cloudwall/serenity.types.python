from uuid import UUID

from serenity_types.utils.serialization import CamelModel


class Asset(CamelModel):
    asset_id: UUID
    """
    Unique, immutable ID for this asset. Symbols can change over time,
    but asset ID's are stable.
    """

    symbol: str
    """
    Serenity's unique symbol for this asset, e.g. tok.usdc.ethereum.
    """
