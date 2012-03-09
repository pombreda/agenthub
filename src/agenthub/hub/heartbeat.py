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

from threading import RLock
from datetime import timedelta
from datetime import datetime as dt
from gofer.messaging import Topic
from gofer.messaging.consumer import Consumer
from logging import getLogger


log = getLogger(__name__)


class HeartbeatManager(Consumer):
    """
    Agent heartbeat listener.
    """

    __status = {}
    __mutex = RLock()

    @classmethod
    def status(cls, uuids=[]):
        """
        Get the agent heartbeat status.
        @param uuids: An (optional) list of uuids to query.
        @return: A tuple (status,last-heartbeat)
        """
        cls.__lock()
        try:
            now = dt.now()
            if not uuids:
                uuids = cls.__status.keys()
            d = {}
            for uuid in uuids:
                last = cls.__status.get(uuid)
                if last:
                    status = ( last[1] > now )
                    heartbeat = last[0].isoformat()
                    any = last[2]
                else:
                    status = False
                    heartbeat = None
                    any = {}
                d[uuid] = (status, heartbeat, any)
            return d
        finally:
            cls.__unlock()

    @classmethod
    def __lock(cls):
        cls.__mutex.acquire()

    @classmethod
    def __unlock(cls):
        cls.__mutex.release()

    def __init__(self, url):
        topic = Topic('heartbeat')
        Consumer.__init__(self, topic, url=url)

    def dispatch(self, envelope):
        try:
            self.__update(envelope.heartbeat)
        except:
            log.exception(envelope)
        self.ack()

    def __update(self, body):
        self.__lock()
        try:
            log.debug(body)
            uuid = body.pop('uuid')
            next = body.pop('next')
            last = dt.now()
            next = int(next*1.20)
            next = last+timedelta(seconds=next)
            self.__status[uuid] = (last, next, body)
        finally:
            self.__unlock()