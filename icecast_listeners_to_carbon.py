#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse

import xml.etree.ElementTree as ET
import requests

import graphitesend

httptimeout = 2.0

def send_stats(host=None, port='8000', user='admin', password='hackme', mountpoint=None, metric=None, graphite_server='127.0.0.1', graphite_port=2003, dry_run=False):

    url = "http://{}:{}/admin/listclients?mount={}".format(host, port, mountpoint)
    req = requests.get(url, auth=(user, password), timeout=httptimeout)

    if req.status_code == 401:
        raise Exception("Authentication Failed.")

    elif req.status_code != 200:
        raise Exception("Unknown Error.")

    try:
        parsed = ET.fromstring(req.text)
        listeners = parsed.find('source/Listeners').text
    except:
        raise Exception("Error parsing xml.")

    if metric is None:
        metric = mountpoint.replace('/', '').replace('.', '-') + '-listeners'

    g = graphitesend.init(graphite_server=graphite_server, graphite_port=graphite_port, prefix='', system_name='', dryrun=dry_run)
    print 'Sent: ', g.send(metric, listeners)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',       required=True, help='Icecast host.',        default='127.0.0.1')
    parser.add_argument('--port',       required=True, help='Icecast port.', type=int)
    parser.add_argument('--user',       required=True, help='Icecast admin user.',  default='admin')
    parser.add_argument('--password',   required=True, help='Icecast admin password.')
    parser.add_argument('--mountpoint', required=True, help='Icecast mountpoint.')

    parser.add_argument('--metric',                    help='Carbon metric name. mountpoint-listeners if not given.')
    parser.add_argument('--graphite-server',           help='Graphite server.',     default='127.0.0.1')
    parser.add_argument('--graphite-port',             help='Graphite port.',       default=2003, type=int)
    parser.add_argument('--dry-run',                   help='Dry run.',             action='store_true')

    args = parser.parse_args()

    send_stats(**vars(args))
