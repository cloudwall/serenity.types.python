from datetime import date, datetime
from enum import Enum
from functools import partial
from typing import Dict, List, Type
from uuid import UUID

from faker import Faker
from pydantic import BaseModel


class BaseModelFaker:
    """
    Helper class that can generate fake Pydantic objects given a class
    using a limited number of automated type fakers, with the ability
    to plug in your own custom fakers if required for more complex types.
    Please do not consider this class to be an endorsement of reflection
    as a programming practice: caveat hackor.
    """
    def __init__(self, custom_field_fakers: Dict[Type, object] = {}):
        self.custom_field_fakers = custom_field_fakers
        self.faker = Faker()
        self._fakers_by_type = {
            bool: self.faker.pybool,
            date: self.faker.date,
            datetime: self.faker.date_time,
            str: self.faker.pystr,
            int: self.faker.random_int,
            float: self.faker.pyfloat,
            UUID: self.faker.uuid4,
        }

    def create_fake_model(self, model_class: Type[BaseModel]):
        init_data = {}
        for field_name, field_schema in model_class.__fields__.items():
            field_type = field_schema.outer_type_
            inner_type = field_schema.type_

            # hacky way to recognize that we are dealing with a Union type
            if hasattr(field_type, '__origin__'):
                if not isinstance(field_type.__origin__, Type):
                    field_type = self._pick_from_list(list(field_type.__args__))
                else:
                    field_type = field_type.__origin__

            field_faker = self._get_type_faker(field_type, inner_type)
            if field_faker:
                init_data[field_name] = field_faker()
            else:
                raise ValueError(f'Unhandled field_type: {field_type}')
        return model_class(**init_data)

    def faker(self):
        return self.faker

    def enum_faker(self, clazz: Type[Enum]):
        return self._pick_from_list(list(clazz))

    def list_faker(self, clazz: Type[List], inner_type: Type):
        num_elems = self.faker.pyint(min_value=1, max_value=5)
        fake_list = [self._get_type_faker(inner_type)() for _ in range(num_elems)]
        return fake_list

    def _get_type_faker(self, clazz: Type, inner_type: Type = None):
        default_field_faker = self._fakers_by_type.get(clazz, None)
        field_faker = self.custom_field_fakers.get(clazz, default_field_faker)
        if field_faker:
            return field_faker
        elif issubclass(clazz, Enum):
            return partial(self.enum_faker, clazz=clazz)
        elif issubclass(clazz, List):
            return partial(self.list_faker, clazz=clazz, inner_type=inner_type)
        elif issubclass(clazz, BaseModel):
            return partial(self.create_fake_model, model_class=clazz)
        else:
            raise ValueError(f'Unhandled inner type: {clazz}')

    def _pick_from_list(self, values: List):
        index = self.faker.pyint(min_value=0, max_value=len(values) - 1)
        return values[index]
