import pytest

from pydantic import ValidationError

from serenity_types.catalog.model import ModelConfiguration, ModelConfigurationSummary
from serenity_types_tests.testutils.serialization import roundtrip


def test_roundtrip_model_objects():
    with pytest.raises(ValidationError):
        # expected: https://github.com/pydantic/pydantic/issues/4874
        roundtrip(ModelConfiguration)
    roundtrip(ModelConfigurationSummary)
