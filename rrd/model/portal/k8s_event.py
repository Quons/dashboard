# -*- coding:utf-8 -*-
# Copyright 2017 Xiaomi, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'Ulric Qin'
from rrd.config import MAINTAINERS
from rrd.model.user import User
from .bean import Bean
from rrd.store import event_db


# 继承了Bean
class K8sEvent(Bean):
    _db = event_db
    _tbl = 'string_events'
    _cols = 'id, type, reason, message, involved_object, source, count, first_time, last_time, created_time, update_time'
    _max_obj_items = 5
    _max_obj_len = 1024

    def __init__(self, _id, _type, reason, message, involved_object, source, count, first_time, last_time, create_time,
                 update_time):
        self.id = _id
        self.type = _type
        self.reason = reason
        self.message = message
        self.involved_object = involved_object
        self.source = source
        self.count = count
        self.first_time = first_time
        self.last_time = last_time
        self.create_time = create_time
        self.update_time = update_time

    @classmethod
    def query(cls, page, limit, query, type):
        where = ''
        params = []
        # 构造查询条件
        if type != 'All' and type != 'None':
            where += ' and ' if where else ''
            where += ' type = %s'
            params.append(type)

        vs = cls.select_vs(where=where, order='last_time desc', params=params, page=page, limit=limit)
        total = cls.total(where=where, params=params)
        return vs, total


def writable(self, login_user):
    # login_user can be str or User obj
    if isinstance(login_user, str):
        login_user = User.get_by_name(login_user)

    if not login_user:
        return False

    if login_user.is_admin() or login_user.is_root():
        return True

    if self.creator == login_user.name:
        return True

    if login_user.name in MAINTAINERS:
        return True

    return False
