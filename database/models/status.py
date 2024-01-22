from enum import Enum


class Status(Enum):
    banned = 0
    user = 1
    admin = 2
    super_admin = 3
