from uuid import UUID

from serenity_types.refdata.asset import Asset


class Currency(Asset):
    """
    An asset representing a fiat currency like the dollar, euro or yen.
    """

    fiat_issuance_id: UUID
    """
    A reference to the Exposure UUID for the underlying fiat currency issuance. This allows
    for a separation of the dollar asset (the thing you can hold in a portfolio, ccy.usd.cash),
    and exposure to the price of the U.S. dollar (ccy.usd), which you might get via a pegged
    asset or even something fancier like a tokenized USD deposit held at Chase or a CBDC.
    """

    iso_currency_code: str
    """
    The ISO currency code, e.g. USD or EUR.
    """
