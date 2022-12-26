from serenity_types.risk.scenarios import (ScenarioCloneRequest,
                                           ScenarioDefinition,
                                           ScenarioRequest,
                                           ScenarioResult,
                                           ScenarioRun)
from serenity_types_tests.testutils.serialization import roundtrip


def test_roundtrip_scenario_objects():
    roundtrip(ScenarioCloneRequest)
    roundtrip(ScenarioDefinition)
    roundtrip(ScenarioRequest)
    roundtrip(ScenarioResult)
    roundtrip(ScenarioRun)
