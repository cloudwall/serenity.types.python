from serenity_types.platform.core import LookupTable
from serenity_types_tests.testutils.serialization import roundtrip


def test_roundtrip_platform_objects():
    roundtrip(LookupTable)
