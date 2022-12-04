from uuid import UUID

from serenity_types.refdata.asset import Asset


class Index(Asset):
    provider_org_id: UUID


class ReferenceIndex(Index):
    """
    An index that tracks or references an exposure. Typically used for settlement purposes
    in derivatives contracts.
    """
    referenced_exposure_id: UUID
