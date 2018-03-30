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


__author__ = 'niean'
from rrd import app
from flask import request, g, render_template, jsonify
from rrd.model.portal.k8s_event import K8sEvent


@app.route('/portal/event')
def k8sevent_get():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 5))
    query = request.args.get('q', '').strip()
    type = request.args.get('type', '')
    vs, total = K8sEvent.query(page, limit, query, type)
    return render_template(
        'portal/event/list.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page,
            'type': type,
        }
    )
