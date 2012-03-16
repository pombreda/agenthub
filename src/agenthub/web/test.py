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
from agenthub.web.http import BadRequest
from agenthub.web.controller import Controller
from gofer.messaging import Options
from logging import getLogger

log = getLogger(__name__)

#
# REST Controllers
#


class Test(Controller):
    
    PATH = '/tmp/hubtest.log'

    def POST(self, x):
        s = []
        body = self.body()
        f = open(self.PATH, 'a+')
        f.write('\n')
        s.append(time.ctime())
        s.append('       sn: %s' % body.get('sn'))
        s.append('      any: %s' % body.get('any'))
        s.append('   status: %s' % body.get('status'))
        s.append('    reply: %s' % body.get('reply'))
        s.append('exception:\n%s' % body.get('exception'))
        f.write('\n'.join(s))
        f.write('\n')
        f.flush()
        f.close()
        self.status(200)

#
# REST Application
#

URLS = (
    '/api/([^/]+)/$', 'Test',
)

application = web.application(URLS, globals())