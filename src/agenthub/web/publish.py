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
from agenthub.web.http import BadRequest
from agenthub.web.controller import Controller
from agenthub.hub.publisher import Publisher
from gofer.messaging import Options

#
# REST Controllers
#


class Publish(Controller):

    def POST(self, topic):
        body = self.body()
        p = Publisher()
        p.publish(topic, body)
        self.status(200)
        
    def body(self):
        body = Controller.body(self)
        if body is None:
            body = {}
        if not isinstance(body, dict):
            raise BadRequest('"body" must be <dict>')
        if not body:
            raise BadRequest('"body" <empty>')
        return body

#
# REST Application
#

URLS = (
    '/([^/]+)/$', 'Publish',
)

application = web.application(URLS, globals())