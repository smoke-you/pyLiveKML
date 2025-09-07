# Update Status

I'm currently working on a major update to v1, with work including:

| Task | Status |
| --- | --- |
| Adding in all of the KML (and KML extension) classes [defined by Google](https://developers.google.com/kml/documentation/kmlreference). | Done |
| Reworking inheritance to minimize the amount of class-specific behaviour. | Done |
| Ensuring that classes can be instantiated directly, as well as via the live feed mechanism using `<NetworkLinkControl>` tags. Added a "simple" eval app to demonstrate this. | Done |
| Simplifying the directory structure of the package. | Done |
| Adding an explanation of how the implementation works. | Done |
| Re-doing all code documentation. | Mostly Done |

## Work in Progress

The `Schema`, and hence `Track` and `MultiTrack` classes, should not be relied upon as yet. Further, no attempt has yet been made to implement `ExtendedData`. All of these require additional work that I will carry out as time permits.

## Changes from version 0

This is a major revision. Code relying upon pyLiveKML will almost certainly need to be re-written to incorporate the changes, particularly around object imports.

# What is pyLiveKML?

pyLiveKML is an implementation of Google's 
[Keyhole Markup Language](https://developers.google.com/kml/documentation/kmlreference) (KML) that enables an 
(approximately) live feed of geospatial information into [Google Earth Pro](https://www.google.com/earth/versions/) 
(GEP). GEP is updated on the fly using an implementation of the mechanism described in 
[Google's documentation](https://developers.google.com/kml/documentation/updates). KML tags are automatically created, updated and deleted as necessary.

pyLiveKML also provides a means of constructing static KML files from Python.

Several simple evaluation apps are included with the pyLiveKML source.  These projects use [Uvicorn](https://www.uvicorn.org/) and [FastAPI](https://fastapi.tiangolo.com/) to serve KML files to GEP, and to serve HTML etc files to provide a user interface via a browser.

# How does pyLiveKML work?

See [how-it-works](https://github.com/smoke-you/pyLiveKML/blob/main/docs/how-it-works.md) for a reasonably detailed explanation.

# Has the entire KML specification been implemented?

From version 1.0.0, all of the KML classes described in the [KML specification](https://developers.google.com/kml/documentation/kmlreference) have been implemented.

# GIS and OS Compatibility

pyLiveKML has been tested:

* Serving to Google Earth Pro on Microsoft Windows 10 with HTTP and HTTPS

* Serving from Python 3.10 on Windows 10

* Serving from Python 3.10 on Ubuntu 22.04

It is possible, even probable, that pyLiveKML will work with other KML-compliant GIS's and/or other operating systems, and/or later versions of Python, but no such alternatives have been researched or tested by the author.

# Evaluation Applications

* [Aircraft Tracer](https://github.com/smoke-you/pyLiveKML/blob/main/evals/apps/aircraft_tracer/README.md)

* [Aircraft Tracker](https://github.com/smoke-you/pyLiveKML/blob/main/evals/apps/aircraft_tracker/README.md)

* [Aircraft Trail](https://github.com/smoke-you/pyLiveKML/blob/main/evals/apps/aircraft_trail/README.md)

* [Geometry](https://github.com/smoke-you/pyLiveKML/blob/main/evals/apps/geometry/README.md)

* [Simple](https://github.com/smoke-you/pyLiveKML/blob/main/evals/apps/simple/README.md)

If GEP is started without any arguments, you will need to add a new NetworkLink object to "Temporary Places", with the link address set to the URI of the loader.kml file, e.g. http(s)://addr:port/loader.kml. GEP will not load loader.kml from the URI using File->Open.  However, if you start GEP with the URI of loader.kml as an argument, then it will load loader.kml on startup.

# Documentation

The code is reasonably thoroughly documented via docstrings.

# Licence

[Gnu Affero GPL v3](https://github.com/smoke-you/pyLiveKML/blob/main/LICENCE)

# Contributions

While I've done a fair bit of testing, particularly with the revision from 0.0.4 to 1.0.0, I have no doubt that there are bugs. If you encounter something that needs to be fixed, please let me know via a [Github](https://github.com/smoke-you/pyLiveKML) Discussion topic and/or a PR.
