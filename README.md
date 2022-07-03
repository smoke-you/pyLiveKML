# What is pyLiveKML?

pyLiveKML is an implementation of Google's 
[Keyhole Markup Language](https://developers.google.com/kml/documentation/kmlreference) (KML) that enables an 
(approximately) live feed of geospatial information into [Google Earth Pro](https://www.google.com/earth/versions/) 
(GEP). GEP is updated on the fly using an implementation of the mechanism described in the 
[KML specification](https://developers.google.com/kml/documentation/updates).

Several simple evaluation apps are included with the pyLiveKML source. These projects use the 
[Flask](https://flask.palletsprojects.com/en/2.1.x/) application server, and its integrated development webserver, to 
construct and publish KML files to GEP. Re these evaluation apps, the reader should be conscious that:
* `<NetworkLinkControl>` KML tags are used to create, change and delete content in GEP.
    * GEP only accepts `<NetworkLinkControl>` tags from an HTTP server for security reasons; local files are forbidden.
    * Any HTTP server that is able to dynamically generate content can be used.
* [Flask](https://flask.palletsprojects.com/en/2.1.x/) is used as the application/webserver for the evaluation apps, but
  the authors of Flask, [Pallet Projects](https://palletsprojects.com/), make it very clear that their development HTTP 
  server is not suitable for production. If you're doing anything more than dev and/or testing, you should probably 
  heed their advice.

# GIS and OS Compatibility

pyLiveKML has been tested only with Google Earth Pro on Microsoft Windows 10. It is possible that it may work with 
other KML-compliant GIS's and/or other operating systems, but that has not been tested by the author and is unknown 
at this time.

# Has the entire KML specification been implemented?

No. Only a subset of the KML classes that are described in the 
[KML specification](https://developers.google.com/kml/documentation/kmlreference) has been implemented at this time; 
see [the pyLiveKML documentation](src/docs/build/html/index.html) for a list.  The subset was chosen based on the 
author's personal experience, i.e. what has proven "useful" to me in the past. The list of supported classes could 
certainly be expanded if there is interest.

# Evaluation Applications

* [Aircraft Tracer](evals/aircraft_tracer/README.md)
* [Aircraft Tracker](evals/aircraft_tracker/README.md)
* [Aircraft Trail](evals/aircraft_trail/README.md)
* [Geometry](evals/geometry/README.md)

# [Documentation](src/docs/build/html/index.html)

# [Licence](LICENCE)

# Contributions

I'm willing to do a certain amount of work expanding the KML classes (and, in some cases, the fields) that are 
supported by pyLiveKML.
