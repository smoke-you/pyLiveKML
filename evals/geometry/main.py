import subprocess
import threading
from typing import Optional

from scipy.spatial.transform import Rotation

from evals.webserver import gep_loader, gep_sync, loader_href, start_webserver
"""
you *MUST* import werkzeug (which is imported by the webserver module) *BEFORE* importing pyproj (which is imported
by the GeoShape module) or debugging crashes.
"""
from GeoEllipse import GeoEllipse
from GeoRing import GeoRing
from GeoShape import GeoShape
from pyLiveKML.KML.GeoCoordinates import GeoCoordinates
from pyLiveKML.KML.KML import AltitudeMode
from pyLiveKML.KML.KMLObjects.Style import Style

origin = GeoCoordinates(lon=-85.844, lat=40.019, alt=1000)
# the GeoShapes that will be manipulated
gpr = GeoRing(
    name='ring',
    origin=GeoCoordinates(lon=origin.lon, lat=origin.lat, alt=origin.alt),
    outer_radius=1000,
    inner_radius=800,
    num_vertices=128,
    border_width=1,
    border_color=0xff0000ff,
    fill_color=0x4000ff00,
    altitude_mode=AltitudeMode.CLAMP_TO_GROUND,
)
gpe = GeoEllipse(
    name='ellipse',
    origin=GeoCoordinates(lon=origin.lon, lat=origin.lat, alt=origin.alt),
    x_radius=1000,
    y_radius=800,
    num_vertices=32,
    border_width=1,
    border_color=0xff0000ff,
    fill_color=0x4000ff00,
    altitude_mode=AltitudeMode.ABSOLUTE,
)
gep_sync.container.append(gpr)
gep_sync.container.append(gpe)


def load_gep():
    gep_loader.name = 'Geometry Demonstrator'
    args = ['C:\\Program Files\\Google\\Google Earth Pro\\client\\googleearth.exe', loader_href]
    subprocess.Popen(args)


help_text = {
    'select': 'The \'[s]elect\' command takes at least one argument:'
              '\n\t* The object index, which must be one of a/all/0/1',
    'deselect': 'The \'[d]eselect\' command takes at least one argument:'
                '\n\t* The object index, which must be one of a/all/0/1',
    'move': 'The \'[m]ove\' command takes at least two arguments:'
            '\n\t* The object index, which must be one of a/all/0/1'
            '\n\t* A bearing (one of n/s/e/w or a float)'
            '\n\t* An optional float distance, in metres (the default is 200m)',
    'rotate': 'The \'[r]otate\' command takes at least two arguments:'
              '\n\t* The object index, which must be one of a/all/0/1'
              '\n\t* A float rotation amount, in degrees',
    'color': 'The \'[c]olor\' command takes at least two arguments:'
             '\n\t* The object index, which must be one of a/all/0/1'
             '\n\t* The target, either [b]order or [f]ill'
             '\n\t* The color, a 32-bit hex integer in ABGR format',
    'help': 'The \'[h]elp\' command shows this help text',
}


def get_targets(arg: str) -> Optional[list[GeoShape]]:
    if arg == 'a' or arg == 'all':
        return [f for f in gep_sync.container if isinstance(f, GeoShape)]
    else:
        try:
            return [f for f in [gep_sync.container[int(arg)]] if isinstance(f, GeoShape)]
        except BaseException as x:
            print(f'Only one of 0/1/a/all are allowed as the object index argument \n{x}', flush=True)
            return None


def select(args: list[str]):
    if args is None or len(args) < 2:
        print(help_text['select'])
        return
    args = args[1:]
    f_gen = get_targets(args[0])
    if f_gen is None:
        return
    for f in f_gen:
        f.select(True, True)
        print(f'Selecting {f}', flush=True)


def deselect(args: list[str]):
    if args is None or len(args) < 2:
        print(help_text['deselect'])
        return
    args = args[1:]
    f_gen = get_targets(args[0])
    if f_gen is None:
        return
    for f in f_gen:
        f.select(False, True)
        print(f'Deselecting {f}', flush=True)


def translate(args: list[str]):
    if len(args) < 3:
        print(help_text['move'])
        return
    args = args[1:]
    f_gen = get_targets(args[0])
    if f_gen is None:
        return
    bearing = float(args[1]) if args[1].isdecimal() \
        else 0 if args[1] == 'n' \
        else 90 if args[1] == 'e' \
        else 180 if args[1] == 's' \
        else 270 if args[1] == 'w' \
        else -1
    if bearing < 0:
        print(f'\'{args[1]}\' is not a valid bearing')
        return
    distance = 200 if len(args) < 3 else float(args[2]) if args[2].isdecimal() else -1
    if distance < 0:
        print(f'\'{args[2]}\' is not a valid distance')
        return
    for f in f_gen:
        f.translate_on_surface(bearing, distance)


def rotate(args: list[str]):
    if len(args) < 3:
        print(help_text['rotate'])
        return
    args = args[1:]
    f_gen = get_targets(args[0])
    if f_gen is None:
        return
    mult = 1.0
    if args[1][0] == '-':
        mult = -1.0
        args[1] = args[1][1:]
    rotation = float(args[1]) * mult if args[1].isdecimal() else 0
    if rotation == 0:
        print('A non-zero decimal value is required for the amount of rotation')
        return
    for f in f_gen:
        f.rotate_shape(Rotation.from_euler('z', rotation, degrees=True))


def set_color(args: list[str]):
    if len(args) < 4:
        print(help_text['color'])
        return
    args = args[1:]
    f_gen = get_targets(args[0])
    if f_gen is None:
        return
    if args[2].isalnum() and len(args[2]) == 8:
        try:
            color = int(args[2], base=16)
        except ValueError:
            print(f'{args[2]} is not a valid hex number')
            return
    else:
        print(f'{args[2]} is not a valid 32-bit hex number')
        return
    for f in f_gen:
        s_gen = [s for s in f.styles if isinstance(s, Style)]
        if args[1] == 'b':
            for s in s_gen:
                s.line_style.color = color
        else:
            for s in s_gen:
                s.poly_style.color = color


def show_help():
    for _, v in help_text.items():
        print(f'{v}')


def main():
    web_thread = threading.Thread(target=start_webserver, daemon=True)
    web_thread.start()

    while True:
        cmd = input('hit me: ').lower()
        args = cmd.split(' ')
        if not args:
            continue
        elif args[0] == 'x':
            break
        elif args[0] == 'load':
            load_gep()
        elif args[0] == 's':
            select(args)
        elif args[0] == 'd':
            deselect(args)
        elif args[0] == 'm':
            translate(args)
        elif args[0] == 'r':
            rotate(args)
        elif args[0] == 'c':
            set_color(args)
        elif args[0] == 'h':
            show_help()
        else:
            print(f'{args[0]} is not a recognized command')

    print('Bye')


if __name__ == '__main__':
    main()
