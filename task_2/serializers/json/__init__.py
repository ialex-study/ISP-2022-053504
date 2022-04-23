import re
import sys
from typing import Any, Union
from parser import ISerializer

sys.path.append("/home/ialex/Documents/ISP-2022-053504/task_2")

NONE_STRING = "null"
TRUE_STRING = "true"
FALSE_STRING = "false"

MONITOR_SYMBOL = "\\"

REGEX_DELETING_PATTERN = r"^[\{\[]\n\t*|\t*[\}\]]$"


class JSON(ISerializer):

    def _serialize_object(self, object: Any, tab_count=1) -> str:
        object_type = type(object)

        if object_type is dict:
            return self._serialize_dict(object, tab_count=tab_count)

        if object_type is list:
            return self._serialize_list(object, tab_count=tab_count)

        if object_type is str:
            return '"' + object.replace('"', f'{MONITOR_SYMBOL}"') + '"'

        if object_type in (int, float):
            return str(object)

        if object_type is type(None):
            return NONE_STRING

        if object_type is bool:
            return TRUE_STRING if object else FALSE_STRING

        raise TypeError(f"Unknown type {object_type}")

    def _serialize_dict(self, object: dict, tab_count=1) -> str:
        result = ""

        TABS = '\t' * tab_count

        for key, value in object.items():
            result += f'{TABS}"{key}": {self._serialize_object(value, tab_count=tab_count + 1)},\n'

        return "{\n" + result.rstrip(",\n") + "\n" + TABS + "}"

    def _serialize_list(self, object: list, tab_count=1) -> str:
        result = ""

        TABS = '\t' * tab_count

        for item in object:
            result += f"{TABS}{self._serialize_object(item, tab_count=tab_count + 1)},\n"

        return "[\n" + result.rstrip(",\n") + "\n" + TABS + "]"

    def _check_value_end(self, char, tmp):
        return char == '"' and len(tmp) > 0 and tmp[-1] != MONITOR_SYMBOL

    def _deserialize_object(self, string: str) -> Any:
        if string.startswith("{"):
            return self._deserialize_dict(string)

        if string.startswith("["):
            return self._deserialize_list(string)

        if string.startswith('"'):
            return string.strip('"').replace(f'{MONITOR_SYMBOL}', '')

        if string == NONE_STRING:
            return None

        if string == TRUE_STRING:
            return True

        if string == FALSE_STRING:
            return False

        if string.find(".") != -1:
            return float(string)

        return int(string)

    def _deserialize_dict(self, string: str) -> dict:
        string = re.sub(REGEX_DELETING_PATTERN, "", string).strip()

        result = {}
        is_key = True
        key = None
        tmp = ""
        char_index = 0
        string_len = len(string)

        brace_count = 0
        bracket_count = 0

        while char_index < string_len:
            char = string[char_index]

            if is_key:
                if self._check_value_end(char, tmp):
                    key = tmp + char

                    tmp = ""
                    is_key = False
                    char_index += 1  # skip ":"

                else:
                    tmp += char

            else:
                if brace_count == bracket_count == 0 and (
                    (
                        tmp.lstrip().startswith('"') and
                        self._check_value_end(char, tmp)
                    ) or
                    (
                        not tmp.startswith('"') and
                        char == ','
                    )
                ):
                    tmp = tmp + char
                    result[self._deserialize_object(
                        key)] = self._deserialize_object(tmp.strip().rstrip(','))

                    tmp = ""
                    is_key = True
                    # find next key start index
                    char_index = string.find('"', char_index + 1) - 1

                    if char_index < 0:
                        break

                else:
                    if char == '{':
                        brace_count += 1
                    if char == '[':
                        bracket_count += 1
                    if char == ']':
                        bracket_count -= 1
                    if char == '}':
                        brace_count -= 1

                    tmp += char

            char_index += 1
        
        if tmp.strip() != "":
            result[self._deserialize_object(
                key)] = self._deserialize_object(tmp.strip())

        return result

    def _deserialize_list(self, string: str) -> list:
        string = re.sub(REGEX_DELETING_PATTERN, "", string)

        result = []
        tmp = ""
        char_index = 0
        string_len = len(string)

        brace_count = 0
        bracket_count = 0

        while char_index < string_len:
            char = string[char_index]

            if brace_count == bracket_count == 0 and (
                (
                    tmp.startswith('"') and
                    self._check_value_end(char, tmp)
                ) or
                (
                    not tmp.startswith('"') and
                    char == ','
                )
            ):
                tmp = tmp + char
                result.append(self._deserialize_object(tmp.strip().rstrip(',')))

                tmp = ""
                char_index = string.find(',', char_index)

                if char_index < 0:
                    break
            
            else:
                if char == '{':
                    brace_count += 1
                if char == '[':
                    bracket_count += 1
                if char == ']':
                    bracket_count -= 1
                if char == '}':
                    brace_count -= 1

                tmp += char

            char_index += 1
        
        if tmp.strip() != "":
            result.append(self._deserialize_object(tmp.strip().rstrip(',')))

        return result

    def dump(self, obj, fp):
        fp.write(self._serialize_object(obj))

    def dumps(self, obj):
        return self._serialize_object(obj)

    def load(self, fp):
        return self._deserialize_object(fp.read())

    def loads(self, s):
        return self._deserialize_object(s)
