from serenity_types.refdata.organization import Organization
from serenity_types_tests.testutils.serialization import roundtrip


def test_roundtrip_org_objects():
    roundtrip(Organization)
