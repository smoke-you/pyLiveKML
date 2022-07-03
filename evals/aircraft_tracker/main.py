import itertools
import json
import subprocess
import threading
from datetime import datetime
from typing import Optional

from AircraftData import AircraftData
from AircraftLocation import AircraftLocation
from evals.webserver import gep_loader, gep_sync, loader_href, start_webserver
from pyLiveKML.KML.KMLObjects.Feature import Feature


def load_adsb_exchange_data(filename: str):
    with open(filename) as f:
        sample_data = json.loads(f.read())
    try:
        transponder = sample_data['icao']
        flight = sample_data['r']
        base_ts = sample_data['timestamp']
        trace = sample_data['trace']
        positions = list[AircraftData]()
        for t in trace:
            try:
                p = AircraftData(
                    datetime.fromtimestamp(base_ts + t[0]),
                    t[2],
                    t[1],
                    t[3] * 0.3048 if isinstance(t[3], (float, int)) else None,
                    t[4] * 1.852 if isinstance(t[4], (float, int)) else 0,
                    t[5] if isinstance(t[5], (float, int)) else 0
                )
                positions.append(p)
            except BaseException as x:
                print(x)
        tracker = AircraftLocation(transponder, flight, positions)
        gep_sync.container.append(tracker)
    except BaseException as x:
        print(x)


def load_gep():
    gep_loader.name = 'Aircraft Track Demonstrator'
    args = ['C:\\Program Files\\Google\\Google Earth Pro\\client\\googleearth.exe', loader_href]
    subprocess.Popen(args)


help_text = {
    'select': 'The \'[s]elect\' command takes at least one argument:'
              '\n\t* The object index, which must be one of a/all/0/1/2',
    'deselect': 'The \'[d]eselect\' command takes at least one argument:'
                '\n\t* The object index, which must be one of a/all/0/1/2',
    'help': 'The \'[h]elp\' command shows this help text',
}


def get_targets(arg: str) -> Optional[list[Feature]]:
    if arg == 'a' or arg == 'all':
        return [f for f in gep_sync.container]
    else:
        try:
            return [f for f in [gep_sync.container[int(arg)]]]
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


def show_help():
    for _, v in help_text.items():
        print(f'{v}')


def main():
    # select any one of the .json track files for display
    load_adsb_exchange_data('..\\aircraft_data\\N921DU-2022-02-01.json')
    load_adsb_exchange_data('..\\aircraft_data\\B1616-2022-02-01.json')
    load_adsb_exchange_data('..\\aircraft_data\\PH-BXC-2022-02-01.json')
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
        elif args[0] == 'h':
            show_help()
        else:
            print(f'{args[0]} is not a recognized command')

    print('Bye')


if __name__ == '__main__':
    main()
