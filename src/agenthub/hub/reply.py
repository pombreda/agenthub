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
from gofer.messaging import Queue, Options
from gofer.rmi.async import ReplyConsumer, Listener
from agenthub.hub.notify import NotifyJournal
from agenthub.web.http import *
from logging import getLogger


log = getLogger(__name__)


class ReplyManager(Listener):

    CTAG = 'AGENTHUB__REPLY'

    def __init__(self, url):
        queue = Queue(self.CTAG)
        self.consumer = ReplyConsumer(queue, url=url)

    def start(self, watchdog):
        self.consumer.start(self, watchdog=watchdog)
        log.info('reply (mgr): started')

    def succeeded(self, reply):
        log.info('succeeded: %s', reply)
        body = dict(
            sn=reply.sn,
            status=(200, HTTP_CODES[200]),
            reply=reply.retval)
        je = dict(
            notify=reply.any,
            body=body)
        self.write(je, reply.sn)
            
    def failed(self, reply):
        log.info('failed: %s', reply)
        try:
            reply.throw()
        except EXCEPTIONS, raised:
            pass
        httpcode = status(raised)
        body = dict(
            sn=reply.sn,
            status=(httpcode, HTTP_CODES[httpcode]),
            exception=str(raised))
        je = dict(
            notify=reply.any,
            body=body)
        fn = '%s.failed' % reply.sn
        self.write(je, fn)
            
    def status(self, reply):
        pass
    
    def write(self, reply, fn):
        path = os.path.join(NotifyJournal.PATH, fn)
        fp = open(path, 'w')
        try:
            json.dump(reply, fp)
        finally:
            fp.close()
