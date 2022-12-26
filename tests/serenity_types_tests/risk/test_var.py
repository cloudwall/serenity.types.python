from serenity_types.risk.var import (VaRAnalysisRequest, VaRAnalysisResult,
                                     VaRBacktestRequest, VaRBacktestResult)
from serenity_types_tests.testutils.serialization import roundtrip


def test_roundtrip_var_objects():
    roundtrip(VaRAnalysisRequest)
    roundtrip(VaRAnalysisResult)
    roundtrip(VaRBacktestRequest)
    roundtrip(VaRBacktestResult)
