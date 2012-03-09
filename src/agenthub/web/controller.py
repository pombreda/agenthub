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
import simplejson as json
from agenthub.web.http import *

class Controller:
    
    def body(self):
        """
        JSON decode the objects in the requests body and return them
        @return: dict of parameters passed in through the body
        """
        data = web.data()
        if not data:
            return {}
        return json.loads(data)

    def header(self, hdr, value, unique=True):
        """
        Adds 'hdr: value' to the response.
        @type hdr: str
        @param hdr: valid http header key
        @type value: str
        @param value: valid value for corresponding header key
        @type unique: bool
        @param unique: whether only one instance of the header is permitted.
        """
        hdr = web.utf8(hdr)
        value = web.utf8(value)
        previous = []
        for h, v in web.ctx.headers:
            if h.lower() == hdr.lower():
                previous.append((h, v))
        if unique:
            for p in previous:
                web.ctx.headers.remove(p)
        web.ctx.headers.append((hdr, value))
        
    def status(self, code):
        web.ctx.status = '%d %s' % (code, HTTP_CODES[code])
    
    def reply(self, code, body):
        self.header(*JSON_HEADER)
        self.status(code)
        return json.dumps(body)
        