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
import simplejson as json
from time import sleep
from threading import Thread
from agenthub.rest import Rest, Basic, NoAuth
from agenthub.hub.config import Config, nvl
from gofer.messaging import Options
from logging import getLogger


log = getLogger(__name__)


class NotifyManager(Thread):
    
    ROOT = '/var/lib/agenthub/journal/notify'
    
    def __init__(self):
        Thread.__init__(self, name='notify')
        self.setDaemon(True)
        
    def run(self):
        log.info('notify (mgr), started')
        while True:
            try:
                self.poll()
            except Exception:
                log.exception(self.ROOT)
                
    def poll(self):
        jnl = NotifyJournal()
        for path in jnl.list():
            self.process(path)
        sleep(1)

    def process(self, path):
        log.info(path)
        try:
            je = self.read(path)
            je = Options(je)
            notify = Options(je.notify)
            system = System(notify.systemid)
            r = system.notify(notify.method, notify.path, je.body)
            os.unlink(path)
        except Exception:
            log.exception(path)
                
    def read(self, path):
        fp = open(path)
        try:
            return json.load(fp)
        finally:
            fp.close()

    def __mkdir(self):
        if not os.path.exists(self.ROOT):
            os.makedirs(self.ROOT)
            
            
class NotifyJournal:
    
    PATH = '/var/lib/agenthub/journal/notify'

    def __init__(self, path=PATH):
        self.path = path
        
    def list(self):
        files = []
        for fn in os.listdir(self.path):
            path = os.path.join(self.path, fn)
            ts = os.path.getctime(path)
            files.append((ts, path))
        files = [p[1] for p in sorted(files)]
        return files


class System:
    
    CONFD = '/etc/agenthub/conf.d'
    
    def __init__(self, id):
        self.id = id
        cfg = self.__cfg()
        self.host = nvl(cfg.main.host, 'localhost')
        self.port = int(nvl(cfg.main.port, 443))
        self.auth = self.__auth(cfg)
        self.root = nvl(cfg.main.root)
    
    def notify(self, method, path, body):
        path = self.join(path)
        rest = Rest(self.host, self.port, self.auth)
        status = rest.request(method, path, body)
        return status

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
