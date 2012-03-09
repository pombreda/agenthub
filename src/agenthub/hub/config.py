#
# Copyright (c) 2011 Red Hat, Inc.
#
# This software is licensed to you under the GNU Lesser General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (LGPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of LGPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.0.txt.
#
# Jeff Ortel <jortel@redhat.com>
#

from iniparse import INIConfig
from iniparse.config import Undefined


MAIN = '/etc/agenthub/hub.conf'


def _undefined(self, name):
    return self

Undefined.__getattr__ = _undefined


def ndef(x):
    """
    Section/property not defined.
    @param x: A section/property
    @type x: A section or property object.
    @return: True if not defined.
    """
    return isinstance(x, Undefined)

def nvl(x, d=None):
    """
    Not define value.
    @param x: An object to check.
    @type x: A section/property
    @return: d if not defined, else x.
    """
    if ndef(x):
        return d
    else:
        return x


class Config(INIConfig):
    
    def __init__(self, path=MAIN):
        fp = open(path)
        try:
            INIConfig.__init__(self, fp)
        finally:
            fp.close()