from serenity_types.risk.factor import (RiskAttributionRequest,
                                        RiskAttributionResponse)
from serenity_types_tests.testutils.serialization import roundtrip


def test_roundtrip_factor_risk_objects():
    roundtrip(RiskAttributionRequest)
    roundtrip(RiskAttributionResponse)
