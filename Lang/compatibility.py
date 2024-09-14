from typing import *

import sys

if(sys.version_info < (3, 11)):
    Self = Any

    from enum import Enum
    class StrEnum(str, Enum):
        ...
