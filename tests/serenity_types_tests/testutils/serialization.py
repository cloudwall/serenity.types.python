from datetime import date, datetime, time
from enum import Enum
from functools import partial
from json import dumps
from typing import Callable, Dict, List, Type
from uuid import UUID

from faker import Faker
from pydantic import BaseModel, Json
from typing_inspect import get_args, get_origin, is_optional_type, is_union_type


class BaseModelFaker:
    """
    Helper class that can generate fake Pydantic objects given a class
    using a limited number of automated type fakers, with the ability
    to plug in your own custom fakers if required for more complex types.
    Please do not consider this class to be an endorsement of reflection
    as a programming practice: caveat hackor.
    """
    def __init__(self, custom_field_fakers: Dict[Type, object] = {},
                 pre_create_hook: Callable[[Dict], Dict] = None):
        self.custom_field_fakers = custom_field_fakers
        self.pre_create_hook = pre_create_hook

        self.faker = Faker()
        self._fakers_by_type = {
            bool: self.faker.pybool,
            date: self.faker.date,
            datetime: self.faker.date_time,
            time: self.faker.time,
            str: self.faker.pystr,
            int: self.faker.random_int,
            float: self.faker.pyfloat,
            Json: self.json_data_faker,
            object: self.json_data_faker,
            UUID: self.faker.uuid4
        }

    def create_fake_model(self, model_class: Type[BaseModel]):
        init_data = {}
        for field_name, field_schema in model_class.__fields__.items():
            field_type = field_schema.outer_type_
            if is_optional_type(field_type):
                # for Optional[T], pick the lead type (not NoneType)
                field_type = get_args(field_type)[0]
            elif is_union_type(field_type):
                # for Unions, pick one type at random
                field_type = self._pick_from_list(get_args(field_type))

            field_faker = self._get_type_faker(field_type)
            init_data[field_name] = field_faker()

        if self.pre_create_hook:
            init_data = self.pre_create_hook(init_data)
        return model_class(**init_data)

    def faker(self):
        return self.faker

    def enum_faker(self, clazz: Type[Enum]):
        return self._pick_from_list(list(clazz))

    def list_faker(self, elem_type: Type):
        num_elems = self.faker.pyint(min_value=1, max_value=5)
        fake_list = [self._get_type_faker(elem_type)() for _ in range(num_elems)]
        return fake_list

    def dict_faker(self, key_type: Type, value_type: Type):
        num_elems = self.faker.pyint(min_value=1, max_value=5)
        fake_dict = {self._get_type_faker(key_type)(): self._get_type_faker(value_type)() for _ in range(num_elems)}
        return fake_dict

    def json_data_faker(self):
        num_elems = self.faker.pyint(min_value=1, max_value=5)
        keys = [self.faker.pystr() for _ in range(num_elems)]
        values = [self.faker.name() for _ in range(num_elems)]
        fake_dict = dict(zip(keys, values))
        return dumps(fake_dict)

    def _get_type_faker(self, clazz: Type):
        default_field_faker = self._fakers_by_type.get(clazz, None)
        origin_type = get_origin(clazz)
        field_faker = self.custom_field_fakers.get(clazz, default_field_faker)
        if field_faker:
            return field_faker
        elif origin_type and issubclass(origin_type, List):
            args = get_args(clazz)
            return partial(self.list_faker, elem_type=args[0])
        elif origin_type and issubclass(origin_type, Dict):
            args = get_args(clazz)
            return partial(self.dict_faker, key_type=args[0], value_type=args[1])
        elif issubclass(clazz, Enum):
            return partial(self.enum_faker, clazz=clazz)
        elif issubclass(clazz, BaseModel):
            return partial(self.create_fake_model, model_class=clazz)
        else:
            raise ValueError(f'Unhandled inner type: {clazz}')

    def _pick_from_list(self, values: List):
        index = self.faker.pyint(min_value=0, max_value=len(values) - 1)
        return values[index]


faker = BaseModelFaker()


def roundtrip(clazz: Type):
    """
    Boilerplate test that just roundtrips and object to
    JSON and back to ensure test coverage of all classes
    and validations. Not a substitute for specific tests
    of edge cases for validators.
    """
    obj = faker.create_fake_model(clazz)
    raw_json = obj.json()
    obj_out = clazz.parse_raw(raw_json)
    assert obj == obj_out
