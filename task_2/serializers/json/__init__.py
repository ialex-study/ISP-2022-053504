import sys
sys.path.append("/home/ialex/Documents/ISP-2022-053504/task_2")

from parser import ISerializer


class JSON(ISerializer):
    def dump(self, obj, fp):
        pass

    def dumps(self, obj):
        pass

    def load(self, fp):
        pass

    def loads(self, s):
        pass