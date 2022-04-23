from typing import IO
from parser import ISerializer
import yaml
import sys

sys.path.insert(0, "/home/ialex/Documents/ISP-2022-053504/task_2")


class YAML(ISerializer):

    def dump(self, obj: dict, fp: IO) -> None:
        yaml.dump(obj, fp)

    def dumps(self, obj: dict) -> str:
        return yaml.dump(obj)

    def load(self, fp: IO) -> dict:
        return yaml.load(fp)

    def loads(self, s: str) -> dict:
        return yaml.load(s)
