# Purpose

This example app is intended to demonstrate:
* Subclassing KML Placemarks, including:
    * Dynamically updating KML object properties, e.g. the LLA coordinates and the `<description>` KML tag.
    * Overriding KML methods to alter how a KML object is published to GEP.

# What Does it Do?

Tracking information from several (up to three) commercial flights is displayed in GEP as individual Placemarks. Each 
aircraft Placemark is created only once, when the aircraft is selected.  The Placemark then moves as the position (LLA) 
and heading data is updated using KML <Change> tags.

Note that playback is not aligned to the timestamps of the data points.  Each time the `<NetworkLink>` loaded into GEP
requests an update, the next point is retrieved from the list.  The update interval is set to 0.5s, but there may be 
considerably more time between points.

# Where did the flight data come from?

The flight data was downloaded from [ADSB Exchange](https://www.adsbexchange.com/data/) under their "Enthusiast Usage 
Terms".  Given the permissive nature of the usage terms, ADSB Exchange have not been formally consulted about this 
project or its usage of their data. Nonetheless, they have my thanks for making that data available.
