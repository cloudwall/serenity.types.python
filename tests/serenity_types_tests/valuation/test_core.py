from serenity_types.valuation.core import PortfolioValuationRequest, PortfolioValuationResponse
from serenity_types_tests.testutils.serialization import roundtrip


def test_roundtrip_valuation_objects():
    roundtrip(PortfolioValuationRequest)
    roundtrip(PortfolioValuationResponse)
