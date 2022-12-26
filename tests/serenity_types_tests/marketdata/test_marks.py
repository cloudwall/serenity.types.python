from serenity_types.marketdata.marks import AssetMarkPrice
from serenity_types_tests.testutils.serialization import roundtrip


def test_roundtrip_marketdata_objects():
    roundtrip(AssetMarkPrice)
