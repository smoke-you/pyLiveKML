"""KMLApp module."""

import importlib
import inspect

from operator import attrgetter
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, UUID4

from pyLiveKML import NetworkLinkControl
from pyLiveKML.KMLObjects.Feature import Feature


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
        self.sync: Optional[NetworkLinkControl] = None

    def load_data(self) -> None:
        """Associate the app's data with the KML synchronization controller."""
        if not self.sync:
            return
        if self.data is not None:
            if isinstance(self.data, Feature):
                if self.data.id not in map(lambda x: x.id, self.sync.container):
                    self.sync.container.append(self.data)
            else:
                for d in self.data:
                    if d.id not in map(lambda x: x.id, self.sync.container):
                        self.sync.container.append(d)


def find_apps(basedir: Path) -> list[KMLApp]:
    """Find all KMLApp instances located under the given path."""
    apps = list[KMLApp]()
    # for file in Path(basedir).rglob("*.py"):
    for file in Path(basedir).rglob("geometry.py"):
        modpath = ".".join(file.parent.parts[-2:]) + "." + file.stem
        try:
            items = inspect.getmembers(importlib.import_module(modpath))
            for _, item in items:
                if isinstance(item, KMLApp):
                    apps.append(item)
        except ModuleNotFoundError:
            pass
    return sorted(apps, key=attrgetter("name"))
