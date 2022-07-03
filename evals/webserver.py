import logging
from typing import Optional

from flask import Flask, make_response
from lxml import etree
from werkzeug.exceptions import abort

from pyLiveKML.KML.KML import RefreshMode, kml_tag, kml_header
from pyLiveKML.KML.KMLObjects.Folder import Folder
from pyLiveKML.KML.KMLObjects.NetworkLink import NetworkLink
from pyLiveKML.KML.NetworkLinkControl import NetworkLinkControl

# configure the webserver and its files
server = Flask('Geospatial Webserver')
server_host = 'localhost'
server_port = 5000
server_uri = f'http://{server_host}:{server_port}/'
elements_file = 'elements.kml'
update_file = 'update.kml'
loader_file = 'loader.kml'
elements_href = f'{server_uri}{elements_file}'
update_href = f'{server_uri}{update_file}'
loader_href = f'{server_uri}{loader_file}'

# The KML loader object; this can be a Document instead if you prefer
gep_loader = Folder(
    name='TBD',
    is_open=True,
    features=[
        NetworkLink(name='Elements', href=elements_href, is_open=True),
        NetworkLink(name='Update', href=update_href, refresh_mode=RefreshMode.ON_INTERVAL, refresh_interval=0.5)
    ]
)

# The master synchronization controller, a NetworkLinkControl object
gep_sync = NetworkLinkControl(target_href=elements_href)


@server.route('/')
@server.route('/<file>')
def webapp_file(file: Optional[str]):
    kml = kml_tag()
    if file == elements_file:
        kml.append(gep_sync.container.construct_kml())
    elif file == update_file:
        kml.append(gep_sync.update_kml())
    elif file == loader_file:
        kml.append(gep_loader.construct_kml(with_features=True))
    else:
        abort(404)
        return

    rsp = etree.tostring(kml, doctype=kml_header, encoding="UTF-8")
    response = make_response(rsp, 200)
    response.headers['Content-Type'] = 'application/vnd.google-earth.kml+xml'
    return response


def start_webserver():
    # Need to disable logging, or the reporting from the webserver interferes with the stdin of the commandline
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    server.run(host=server_host, port=server_port)
