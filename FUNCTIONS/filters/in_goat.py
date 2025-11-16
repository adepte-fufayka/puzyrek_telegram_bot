from CLASSES import UserProfile
from CONSTANTS import GOAT_BAND_NAMES

def is_in_goat(user:UserProfile):
    return user.gang_name in GOAT_BAND_NAMES