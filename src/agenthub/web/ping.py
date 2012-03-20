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
import time
from agenthub.web.controller import Controller
from logging import getLogger

log = getLogger(__name__)

#
# REST Controllers
#


class Ping(Controller):
    
    def GET(self):
        log.info('ping')
        return self.reply(200, time.ctime())

    def POST(self):
        log.info('ping')
        return self.reply(200, self.body())
    
    def PUT(self):
        log.info('ping')
        return self.reply(200, self.body())
    
    def DELETE(self):
        log.info('ping')
        self.status(200)

#
# REST Application
#

URLS = (
    '/$', 'Ping',
)

application = web.application(URLS, globals())