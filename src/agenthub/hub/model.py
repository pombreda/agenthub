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

from gofer.messaging import Options
from agenthub.web.http import BadRequest


class Option:
    
    def __init__(self, opts):
        self.opts = opts or {}
        
    def valid(self):
        if not isinstance(self.opts, dict):
            raise BadRequest('"options" must be <dict>')
        return Options(self.opts)

   
class Request:
    """
    The RMI (call) request model object.
    options = {},
    request = {
      cntr = ([],{}),
      args = [],
      kwargs = {}
    }
    replyto = {
      path = '',
      method='',
      systemid = '',
    }
    any = {}
    """
    
    def __init__(self, request):
        self.request = request
        
    def valid(self):
        request = self.request
        if not request:
            request = {}
        if not isinstance(request, dict):
            raise BadRequest('"request" must be <dict>')
        request = Options(request)
        self.cntr(request)
        self.args(request)
        self.kwargs(request)
        return request

    def cntr(self, request):
        cntr = request.cntr
        if cntr:
            if not isinstance(cntr, list):
                raise BadRequest('"cntr" must be <list>')
            if len(cntr) != 2:
                raise BadRequest('"cntr" must be <list>[2]')
            if not isinstance(cntr[0], list):
                raise BadRequest('"cntr[0]" must be <list>')
            if not isinstance(cntr[1], dict):
                raise BadRequest('"cntr[1]" must be <dict>')
        else:
            cntr = ([],{})
            request.cntr = cntr
        return cntr
            
    def args(self, request):
        args = request.args
        if args:
            if not isinstance(args, list):
                raise BadRequest('"args" must be <list>')
        else:
            args = []
            request.args = args
        return args
    
    def kwargs(self, request):
        kwargs = request.kwargs
        if kwargs:
            if not isinstance(args, dict):
                raise BadRequest('"kwargs" must be <dict>')
        else:
            kwargs = {}
            request.kwargs = kwargs
        return kwargs
    

class ReplyTo:
    """
    The replyto model object.
    replyto = {
      path = '',
      method = (GET|POST|..)
      systemid = '',
    }
    """
    
    METHOD = (
        'GET',
        'POST',
        'PUT',
        'DELETE',)
    
    def __init__(self, replyto):
        self.replyto = replyto
        
    def valid(self):
        replyto = self.replyto
        if replyto is None:
            return
        if not isinstance(replyto, dict):
            raise BadRequest('"replyto" must be <dict>')
        replyto = Options(replyto)
        self.method(replyto)
        self.path(replyto)
        self.systemid(replyto)
        return replyto
    
    def method(self, replyto):
        valid = self.METHOD
        # http method
        if not isinstance(replyto.method, basestring):
            raise BadRequest()
        if replyto.method not in valid:
            raise BadRequest('method must be %s' % valid)
    
    def path(self, replyto):
        if not isinstance(replyto.path, basestring):
            raise BadRequest('"path" must be <str>')
        if not replyto.path:
            raise BadRequest('"path" length < 0')
    
    def systemid(self, replyto):
        if not isinstance(replyto.systemid, basestring):
            raise BadRequest('"systemid" must be <str>')
        if not replyto.systemid:
            raise BadRequest('"systemid" length < 0')