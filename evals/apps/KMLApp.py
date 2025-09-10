"""KMLApp module."""

import importlib
import inspect

from operator import attrgetter
from pathlib import Path
from typing import Iterable, Iterator

from fastapi import FastAPI
from pydantic import BaseModel, UUID4

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
