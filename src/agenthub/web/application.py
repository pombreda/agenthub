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
import logging
from agenthub.web import main
from agenthub.web import publish
from agenthub.web import test
from agenthub.hub.main import Services

#
# REST Application
#

URLS = (
    '/agent', main.application,
    '/publish', publish.application,
    '/test', test.application,
)

Services.start()
def wsgi_application():
    application = web.subdir_application(URLS)
    appfn = application.wsgifunc()
    return appfn
