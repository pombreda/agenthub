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

from gofer import proxy
from gofer.messaging import Options
from gofer.messaging.broker import Broker
from gofer.rmi.async import WatchDog
from agenthub.hub.config import Config, nvl
from agenthub.hub.heartbeat import HeartbeatManager
from agenthub.hub.reply import ReplyManager
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
    started = False

    @classmethod
    def start(cls, url=URL):
        if not cls.started:
            cls.__init(url)
            cls.__start(url)
            cls.started = True
            
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


class Agent:
    
    @classmethod
    def status(cls, uuids=[]):
        return Services.heartbeat.status(uuids)
    
    def __init__(self, uuid, options):
        self.uuid = uuid
        self.options = options or {}
        
    def call(self, cls, method, request, replyto):
        options = Options(self.options)
        if replyto:
            options.ctag = ReplyManager.CTAG
            options.watchdog = Services.watchdog
            options.any = replyto
        log.info('OPTIONS: %s', options)
        agent = proxy.agent(self.uuid, **options)
        clsobj = getattr(agent, cls)
        inst = clsobj()
        cntr = request.cntr
        if cntr:
            inst(*cntr[0], **cntr[1])
        fn = getattr(inst, method)
        return fn(*request.args, **request.kwargs)        
