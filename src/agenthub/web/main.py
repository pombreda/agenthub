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

import web
from agenthub.web import *
from agenthub.web.http import *
from agenthub.web.controller import Controller
from agenthub.hub.main import Agent as AgentFacade
from agenthub.hub.model import *
from gofer.messaging import Options
from logging import getLogger


log = getLogger(__name__)


#
# REST Controllers
#

class Agent(Controller):
    
    def GET(self, uuid):
        status = AgentFacade.status([uuid])
        return self.reply(200, status)
        
        
class Agents(Controller):
    
    def GET(self):
        status = AgentFacade.status()
        return self.reply(200, status)


class Call(Controller):

    def POST(self, uuid, cls, method):
        reply = {}
        httpcode = 200
        try:
            body = self.body()
            options = body.options
            request = Request(body.request)
            request = request.valid()
            replyto = ReplyTo(body.replyto)
            replyto = replyto.valid()
            any = body.any
            agent = AgentFacade(uuid, options)
            reply = agent.call(cls, method, request, replyto, any)
        except EXCEPTIONS, raised:
            reply = str(raised)
            httpcode = status(raised)
        except Exception, raised:
            httpcode = 500
            reply = str(raised)
        return self.reply(httpcode, reply)

    def body(self):
        body = Controller.body(self)
        if body is None:
            body = {}
        if not isinstance(body, dict):
            raise BadRequest('"body" must be <dict>')
        return Options(body)

#
# REST Application
#

URLS = (
    '/$', 'Agents',
    '/([^/]+)/$', 'Agent',
    '/([^/]+)/call/([^/]+)/([^/]+)/$', 'Call',
)

application = web.application(URLS, globals())