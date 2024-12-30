from enum import Enum


class HashMethod(str, Enum):
    MD5 = "md5"
    SHA1 = "sha-1"


class TrialStatus(str, Enum):
    NOT_CALCULATED = "NOT_CALCULATED"
    RESERVED = "RESERVED"
    DONE = "DONE"
