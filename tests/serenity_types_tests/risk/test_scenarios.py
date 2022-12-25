from typing import Type

from serenity_types.risk.scenarios import (ScenarioCloneRequest,
                                           ScenarioDefinition,
                                           ScenarioRequest,
                                           ScenarioResult,
                                           ScenarioRun)
from serenity_types_tests.testutils.serialization import BaseModelFaker


def test_roundtrip_objects():
    faker = BaseModelFaker()

    def roundtrip(clazz: Type):
        obj = faker.create_fake_model(clazz)
        raw_json = obj.json()
        obj_out = clazz.parse_raw(raw_json)
        assert obj == obj_out

    roundtrip(ScenarioCloneRequest)
    roundtrip(ScenarioDefinition)
    roundtrip(ScenarioRequest)
    roundtrip(ScenarioResult)
    roundtrip(ScenarioRun)
