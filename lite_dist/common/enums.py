from enum import Enum


class HashMethod(str, Enum):
    DEFAULT = "default"
    MD5 = "md5"
    SHA1 = "sha-1"
    SHA256 = "sha-256"


class TrialStatus(str, Enum):
    NOT_CALCULATED = "NOT_CALCULATED"
    RESERVED = "RESERVED"
    DONE = "DONE"
    RESOLVED = "RESOLVED"


class TrialSuggestMethod(str, Enum):
    SEQUENTIAL = "sequential"
