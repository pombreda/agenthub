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


class Request:
    """
    The RMI (call) request model object.
    options = {},
    request = {
      constructor = ([],{}),
      args = [],
      kwargs = {}
    }
    replyto = {
      path = '',
      method='',
      systemid = '',
    }
    """
    
    def __init__(self, request):
        self.request = request
        
    def valid(self):
        """
        Get a validated options object.
        @return: A valid object.
        @rtype: L{Options}
        """
        request = self.request
        if not request:
            request = {}
        if not isinstance(request, dict):
            raise BadRequest()
        request = Options(request)
        self.cntr(request)
        self.args(request)
        self.kwargs(request)
        return request

    def cntr(self, request):
        cntr = request.constructor
        if cntr:
            if not isinstance(cntr, list):
                raise BadRequest()
            if len(cntr) != 2:
                raise BadRequest()
            if not isinstance(cntr[0], list):
                raise BadRequest()
            if not isinstance(cntr[1], dict):
                raise BadRequest()
        else:
            cntr = ([],{})
            request.constructor = cntr
        return cntr
            
    def args(self, request):
        args = request.args
        if args:
            if not isinstance(args, list):
                raise BadRequest()
        else:
            args = []
            request.args = args
        return args
    
    def kwargs(self, request):
        kwargs = request.kwargs
        if kwargs:
            if not isinstance(args, dict):
                raise BadRequest()
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
    
    def __init__(self, replyto):
        self.replyto = replyto
        
    def valid(self):
        replyto = self.replyto
        if replyto is None:
            return
        if not isinstance(replyto, dict):
            raise BadRequest()
        replyto = Options(replyto)
        self.method(replyto)
        self.path(replyto)
        self.systemid(replyto)
        return replyto
    
    def method(self, replyto):
        # http method
        if not isinstance(replyto.method, basestring):
            raise BadRequest()
        if not replyto.method:
            raise BadRequest()
    
    def path(self, replyto):
        if not isinstance(replyto.path, basestring):
            raise BadRequest()
        if not replyto.path:
            raise BadRequest()
    
    def systemid(self, replyto):
        if not isinstance(replyto.systemid, basestring):
            raise BadRequest()
        if not replyto.systemid:
            raise BadRequest()