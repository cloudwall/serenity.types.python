from serenity_types.refdata.network import Network
from serenity_types_tests.testutils.serialization import roundtrip


def test_roundtrip_network_objects():
    roundtrip(Network)
