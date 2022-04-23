import toml
import sys
from typing import IO, Any, Union
from parser import ISerializer
from .constants import STRING_TO_OBJECT_DICT, OBJECT_TO_STRING_DICT

sys.path.insert(0, "/home/ialex/Documents/ISP-2022-053504/task_2")


class TOML(ISerializer):

    def _adapt_object_dict(self, object: Any):
        object_type = type(object)

        if object_type is dict:
            result = {}

            for key, value in object.items():
                result[key] = self._adapt_object_dict(value)

            return result

        elif object_type is list:
            return [self._adapt_object_dict(item) for item in object]

        elif object_type in OBJECT_TO_STRING_DICT:
            return {
                OBJECT_TO_STRING_DICT[object_type]: str(object)
            }
        elif object_type is type(None):
            return {
                "None": "None"
            }

    def _restore_object_dict(self, object: Any):
        object_type = type(object)

        if object_type is dict:
            if len(object.keys()) == 1:
                key, value = list(object.items())[0]

                if key == "None":
                    return None
                elif key in STRING_TO_OBJECT_DICT:
                    return STRING_TO_OBJECT_DICT[key](value)

            result = {}
            for key, value in object.items():
                result[key] = self._restore_object_dict(value)

            return result
        else:
            return [self._restore_object_dict(item) for item in object]

    def dump(self, obj: dict, fp: IO) -> None:
        toml.dump(self._adapt_object_dict(obj), fp)

    def dumps(self, obj: dict) -> str:
        return toml.dumps(self._adapt_object_dict(obj))

    def load(self, fp: IO) -> dict:
        return self._restore_object_dict(toml.load(fp))

    def loads(self, s: str) -> dict:
        return self._restore_object_dict(toml.loads(s))
