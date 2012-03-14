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

from gofer.messaging.broker import Broker
from gofer.rmi.async import WatchDog
from agenthub.hub.config import Config, nvl
from agenthub.hub.heartbeat import HeartbeatManager
from agenthub.hub.reply import ReplyManager
from agenthub.hub.notify import NotifyManager
from agenthub.hub.logutil import getLogger

log = getLogger(__name__)
cfg = Config()

#
# Services
#

URL = cfg.broker.url

class Services:
    
    reply = None
    watchdog = None
    heartbeat = None
    notify = None

    @classmethod
    def start(cls, url=URL):
        cls.__init(url)
        cls.__start(url)
            
    @classmethod
    def __init(cls, url):
        b = Broker(url)
        b.cacert = nvl(cfg.broker.cacert)
        b.clientcert = nvl(cfg.broker.clientcert)
            
    @classmethod
    def __start(cls, url):
        cls.watchdog = WatchDog(url=url)
        cls.watchdog.start()
        cls.reply = ReplyManager(url)
        cls.reply.start(cls.watchdog)
        cls.heartbeat = HeartbeatManager(url)
        cls.heartbeat.start()
        cls.notify = NotifyManager()
        cls.notify.start()
