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

class Agent:
    
    ROOT = '/agenthub/agent/'
    
    def __init__(self, uuid, rest, **options):
        self.uuid = uuid
        self.rest = rest
        self.options = options
    
    def __getattr__(self, name):
        return Stub(self, name)


class Stub:
    
    def __init__(self, agent, name):
        self.agent = agent
        self.name = name
        self.cntr = ([],{})

    def __getattr__(self, name):
        return Method(self, name)
    
    def __call__(self, *args, **kwargs):
        self.cntr = (args, kwargs)
        return self


class Method:
    
    def __init__(self, stub, name):
        self.stub = stub
        self.name = name

    def __call__(self, *args, **kwargs):
        options = dict(self.stub.agent.options)
        replyto = options.pop('replyto', None)
        body = {
            'options':options,
            'replyto':replyto,
            'request':{
                'cntr':self.stub.cntr,
                'args':args,
                'kwargs':kwargs,
            }
        }
        path = self.__path()
        reply = self.__rest().post(path, body)
        return reply
    
    def __path(self):
        path = []
        path.append('/agenthub/agent')
        path.append(self.stub.agent.uuid)
        path.append('call')
        path.append('%s' % self.stub.name)
        path.append('%s/' % self.name)
        return '/'.join(path)
    
    def __rest(self):
        return self.stub.agent.rest
