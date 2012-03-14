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
from agenthub.hub.services import Services
from agenthub.hub.reply import ReplyManager
from logging import getLogger

log = getLogger(__name__)


class Agent:

    @classmethod
    def status(cls, uuids=[]):
        return Services.heartbeat.status(uuids)
    
    def __init__(self, uuid, options):
        self.uuid = uuid
        self.options = options or {}
        
    def call(self, cls, method, request, replyto, any):
        options = Options(self.options)
        if replyto:
            options.ctag = ReplyManager.CTAG
            options.watchdog = Services.watchdog
            options.any = dict(any=any, replyto=replyto)
        agent = proxy.agent(self.uuid, **options)
        clsobj = getattr(agent, cls)
        inst = clsobj()
        cntr = request.cntr
        if cntr:
            inst(*cntr[0], **cntr[1])
        fn = getattr(inst, method)
        return fn(*request.args, **request.kwargs)        
