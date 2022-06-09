import math
import yaml
from common.config import config


class DataTransformer:
    def __init__(self, data: dict):
        self._schema = config.data_schema
        self.data = self._scrubber(data)
        self.missing, self.valid = self._check_valid()
        self.data = self._zero_nulls(self.data)
        self.data = self._type_converter(self.data)

    def _scrubber(self, data):
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = v.replace(",", "")
        return data

    def _type_converter(self, data):
        types = {"float": float, "str": str}
        for k, v in self._schema.items():
            t = types[self._schema[k]["type"]]
            data[k] = t(data[k])
        return data

    def _check_valid(self):
        missing = []
        for k in self._schema.keys():
            if self._schema[k]["required"] and self._isempty(
                self.data[k]
            ):
                missing.append(k)
        if missing:
            return missing, False
        else:
            return [], True

    def _zero_nulls(self, data):
        for k, v in data.items():
            if self._isempty(v):
                data[k] = 0
        return data

    def _isempty(self, field):
        if isinstance(field, float) and math.isnan(field):
            return True
        elif field == "" or field is None:
            return True
        else:
            return False

