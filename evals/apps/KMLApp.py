"""KMLApp module."""

import importlib
import inspect

from operator import attrgetter
from pathlib import Path
from typing import Optional

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
        self.data = data
        self.sync: Container

    def load_data(self) -> None:
        """Associate the app's data with the KML synchronization controller."""
        if self.sync is None:
            return
        if self.data is not None:
            if isinstance(self.data, Feature):
                if self.data.id not in map(lambda x: x.id, self.sync):
                    self.sync.append(self.data)
            else:
                for d in self.data:
                    if d.id not in map(lambda x: x.id, self.sync):
                        self.sync.append(d)


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
