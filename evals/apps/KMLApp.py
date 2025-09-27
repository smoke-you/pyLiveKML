# pyLiveKML: A python library that streams geospatial data using the KML protocol.
# Copyright (C) 2022 smoke-you

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""KMLApp module."""

import importlib
import inspect
from operator import attrgetter
from pathlib import Path
from typing import Iterable, Iterator

from fastapi import FastAPI
from pydantic import UUID4, BaseModel

from pyLiveKML.objects.Container import Container
from pyLiveKML.objects.Feature import Feature


class KMLSelect(BaseModel):
    """KML select message."""

    id: UUID4
    checked: bool


class KMLControlRequest(BaseModel):
    """KML control request."""

    req: dict


class KMLControlResponse(BaseModel):
    """KML control response."""

    rsp: dict


class KMLApp:
    """KML application.

    KML applications will appear in the list of available apps in the server's home page.
    """

    def __init__(
        self,
        name: str,
        description: str,
        path: str,
        app: FastAPI,
        data: Feature | list[Feature] | None = None,
    ):
        """KMLApp instance constructor."""
        self.name = name
        self.description = description.strip().replace("\r", "").split("\n")
        self.path = path
        self.app = app
        self._data = list[Feature]()
        self.data = data
        self.sync: Container

    @property
    def data(self) -> Iterator[Feature]:
        """Generator over display data."""
        yield from self._data

    @data.setter
    def data(self, value: Feature | Iterable[Feature] | None) -> None:
        self._data.clear()
        if value is not None:
            if isinstance(value, Feature):
                self._data.append(value)
            else:
                self._data.extend(value)


def find_apps(basedir: Path) -> list[KMLApp]:
    """Find all KMLApp instances located under the given path."""
    apps = list[KMLApp]()
    # for file in Path(basedir).rglob("geometry.py"):
    # for file in Path(basedir).rglob("tracker.py"):
    for file in Path(basedir).rglob("*.py"):
        modpath = ".".join(file.parent.parts[-2:]) + "." + file.stem
        try:
            items = inspect.getmembers(importlib.import_module(modpath))
            for _, item in items:
                if isinstance(item, KMLApp):
                    apps.append(item)
        except ModuleNotFoundError:
            pass
    return sorted(apps, key=attrgetter("name"))
