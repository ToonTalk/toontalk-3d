# Shared vocabulary for the device worlds.
#
# A DEVICE NEST is an ordinary nest wearing one of the workshop's own guids.
# Anything wearing that guid gets the mail, so a world can carry one and it is
# wired up the moment it loads -- there is nothing to connect.
#
# They arrive with no egg, which is what makes them read-only: a bird is the
# only way anything is ever put on a nest, and no bird can be had from an
# eggless one.
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'infinity'))
from _tt import *                                          # noqa: F403,F401

HERE = os.path.dirname(os.path.abspath(__file__))

DEV_KEYS = 'dev-keyboard'
DEV_POINT = 'dev-pointer'
DEV_PRESS = 'dev-press'

WILDTEXT = {'kind': 'wildText'}


def device(nid, guid, label):
    return {'kind': 'nest', 'id': nid, 'guid': guid, 'hasEgg': False,
            'dev': True, 'label': label, 'pile': []}


def write_devices(name, bench):
    return write(name, bench, HERE)                        # noqa: F405
