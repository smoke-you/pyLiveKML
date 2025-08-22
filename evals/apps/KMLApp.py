import importlib
import inspect

from operator import attrgetter
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, UUID4

from pyLiveKML import NetworkLinkControl, Feature


class KMLSelect(BaseModel):
    id: UUID4
    checked: bool


class KMLControlRequest(BaseModel):
    req: dict


class KMLControlResponse(BaseModel):
    rsp: dict


class KMLApp:
    def __init__(
        self,
        name: str,
        description: str,
        path: str,
        app: FastAPI,
        data: Feature | list[Feature],
    ):
        self.name = name
        self.description = description.strip().replace("\r", "").split("\n")
        self.path = path
        self.app = app
        self.data = data
        self.sync: Optional[NetworkLinkControl] = None

    def load_data(self) -> None:
        if not self.sync:
            return
        if isinstance(self.data, Feature):
            if self.data.id not in map(lambda x: x.id, self.sync.container):
                self.sync.container.append(self.data)
        else:
            for d in self.data:
                if d.id not in map(lambda x: x.id, self.sync.container):
                    self.sync.container.append(d)


def find_apps(basedir: Path) -> list[KMLApp]:
    apps = list[KMLApp]()
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
