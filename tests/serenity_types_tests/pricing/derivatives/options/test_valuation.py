from typing import Dict

from serenity_types.pricing.derivatives.options.valuation import OptionValuationRequest, OptionValuationResult
from serenity_types.pricing.derivatives.options.volsurface import (VolatilitySurfaceAvailability,
                                                                   VolatilitySurfaceVersion)
from serenity_types.pricing.derivatives.rates.yield_curve import YieldCurveAvailability, YieldCurveVersion

from serenity_types_tests.testutils.serialization import BaseModelFaker, roundtrip


def test_roundtrip_option_valuation_request():
    # workaround because the default object faker
    # will populate all fields and break validation
    # for cases where you can have neither field set
    # or one set, but not both
    def pre_create_hook(model_data: Dict) -> Dict:
        keys_to_delete = ['yield_curve', 'vol_surface']
        for key in keys_to_delete:
            if key in model_data:
                del model_data[key]
        return model_data

    faker = BaseModelFaker(pre_create_hook=pre_create_hook)
    obj = faker.create_fake_model(OptionValuationRequest)
    raw_json = obj.json()
    obj_out = OptionValuationRequest.parse_raw(raw_json)
    assert obj == obj_out


def test_roundtrip_other_valuation_objects():
    roundtrip(OptionValuationResult)
    roundtrip(VolatilitySurfaceAvailability)
    roundtrip(VolatilitySurfaceVersion)
    roundtrip(YieldCurveAvailability)
    roundtrip(YieldCurveVersion)
