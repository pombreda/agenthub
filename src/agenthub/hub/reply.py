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

import os
from gofer.messaging import Queue, Options
from gofer.rmi.async import ReplyConsumer, Listener
from agenthub.web.http import *
from agenthub.hub.config import Config, nvl
from agenthub.hub.rest import Rest, Basic, NoAuth
from logging import getLogger


log = getLogger(__name__)


class ReplyManager(Listener):

    CTAG = 'AGENTHUB__REPLY'

    def __init__(self, url):
        queue = Queue(self.CTAG)
        self.consumer = ReplyConsumer(queue, url=url)

    def start(self, watchdog):
        self.consumer.start(self, watchdog=watchdog)
        log.info('watchdog: started')

    def succeeded(self, reply):
        log.info('succeeded: %s', reply)
        try:
            replyto = Options(reply.any)
            method = replyto.method
            path = replyto.path
            systemid = replyto.systemid
            peer = Peer(systemid)          
            path = peer.join(path)
            rest = peer.rest()
            r = rest.request(method, path, reply.retval)
            log.info('(%s) %s', path, r)
        except Exception:
            log.exception(reply)

    def failed(self, reply):
        log.info('failed: %s', reply)
        try:
            reply.throw()
        except EXCEPTIONS, raised:
            pass
        try:
            self.__failed(reply, raised)
        except Exception:
            log.exception(reply)
            
    def __failed(self, reply, raised):
        replyto = Options(reply.any)
        method = replyto.method
        path = replyto.path
        systemid = replyto.systemid
        peer = Peer(systemid)          
        path = peer.join(path)
        httpcode = status(raised)
        reply = dict(
            status=(httpcode, HTTP_CODES[httpcode]),
            exception=str(raised))         
        rest = peer.rest()
        r = rest.request(method, path, reply)
        log.info('(%s) %s', path, r)

    def status(self, reply):
        pass


class Peer:
    
    CONFD = '/etc/agenthub/conf.d'
    
    def __init__(self, id):
        self.id = id
        cfg = self.__cfg()
        self.host = nvl(cfg.main.host, 'localhost')
        self.port = int(nvl(cfg.main.port, 443))
        self.auth = self.__auth(cfg)
        self.root = nvl(cfg.main.root)
    
    def rest(self):
        rest = Rest(self.host, self.port, self.auth)
        return rest
        
    def join(self, path):
        if self.root:
            return ''.join((self.root, path))
        else:
            return path
        
    def __auth(self, cfg):
        auth = nvl(cfg.main.auth)
        if not auth:
            return NoAuth()
        if auth == 'basic':
            basic = cfg.basic
            return Basic(basic.user, basic.password)
        
    def __cfg(self):
        fn = '.'.join((self.id, 'conf'))
        path = os.path.join(self.CONFD, fn)
        cfg = Config(path)
        return cfg
    
    def __str__(self):
        s = []
        s.append('host=%s' % self.host)
        s.append('port=%s' % self.port)
        s.append('root=%s' % self.root)
        s.append('auth=%s' % self.auth)
        return ','.join(s)