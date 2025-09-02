# PyPi

The current version on PyPi is 0.0.4, from August 2022.  I can't update it (yet) because I can't access my PyPi account (yet).  Hopefully soon, pretty please PyPi :)

# Currency, in General

I'm currently working on a major update to 1.0.0, including:

1. Adding in all of the KML (and KML extension) classes defined by Google.

2. Reworking inheritance to minimize the amount of class-specific behaviour.

3. Ensuring that classes can be instantiated directly, as well as via the live feed mechanism using `<NetworkLinkControl>` tags. Added a "simple" eval app to this end.

The update work has completely broken the live update mechanism, and invalidated much of the documentation (such as it was). Live update will be restored before the 1.0.0 release, but documentation may trail somewhat.

# What is pyLiveKML?

pyLiveKML is an implementation of Google's 
[Keyhole Markup Language](https://developers.google.com/kml/documentation/kmlreference) (KML) that enables an 
(approximately) live feed of geospatial information into [Google Earth Pro](https://www.google.com/earth/versions/) 
(GEP). GEP is updated on the fly using an implementation of the mechanism described in 
[Google's documentation](https://developers.google.com/kml/documentation/updates). KML tags are automatically created, updated and deleted as necessary.

Several simple evaluation apps are included with the pyLiveKML source.  These projects use [Uvicorn](https://www.uvicorn.org/) and [FastAPI](https://fastapi.tiangolo.com/) to serve KML files to GEP, and to serve HTML etc files to provide a user interface via a browser.

# Has the entire KML specification been implemented?

No. Only a subset of the KML classes that are described in the 
[KML specification](https://developers.google.com/kml/documentation/kmlreference) has been implemented at this time; 
see [the pyLiveKML documentation](src/docs/build/html/index.html) for a list.  The subset was chosen based on the 
author's personal experience, i.e. what has proven "useful" to me in the past. The list of supported classes could 
certainly be expanded.

# GIS and OS Compatibility

pyLiveKML has been tested:
* Serving to Google Earth Pro on Microsoft Windows 10 with HTTP and HTTPS
* Serving from Python 3.10 on Windows 10
* Serving from Python 3.10 on Ubuntu 22.04

It is possible that pyLiveKML may work with other KML-compliant GIS's and/or other operating systems, but no such alternatives have been researched or tested by the author.

# Evaluation Applications

* [Aircraft Tracer](evals/apps/aircraft_tracer/README.md)
* [Aircraft Tracker](evals/apps/aircraft_tracker/README.md)
* [Aircraft Trail](evals/apps/aircraft_trail/README.md)
* [Geometry](evals/apps/geometry/README.md)

It will likely be necessary to set the PYTHONPATH environment variable before running the eval server as-is from the commandline:

* Windows: `set PYTHONPATH=<pyLiveKML root path>`
* Linux: `export PYTHONPATH=<pyLiveKML root path>`

If GEP is started without any arguments, you will need to add a new NetworkLink object to "Temporary Places", with the link address set to the URI of the loader.kml file, e.g. http(s)://addr:port/loader.kml. GEP will not load loader.kml from the URI using File->Open.  However, if you start GEP with the URI of loader.kml as an argument, then it will load loader.kml on startup.

# [Documentation](src/docs/build/html/index.html)

# [Licence](LICENCE)

# Contributions

I'm willing to do a certain amount of work expanding the KML classes and attributes that are supported by pyLiveKML.

If you want me to write a customized server implementation and/or another format of UI, that would be paid work.
