# Purpose

This example app is intended to demonstrate:
* Subclassing KML Folders and Placemarks, including:
    * Overriding KML methods to change the way that a KML object is published to GEP
* Deleting (as opposed to deselecting) KML objects
    * Specifically, the subclassed Placemarks, but the principle is extensible to any Object, i.e. any KML element that 
    has an ID. 

# What Does it Do?

Tracking information from several (up to three) commercial flights is published to GEP as a moving window of contiguous 
positions (Placemarks) under individual Folders, one Folder per selected aircraft.  Placemarks are not changed; rather, 
as the window moves, leading Placemarks are created and trailing Placemarks are deleted.  

Note that playback is not aligned to the timestamps of the data points.  Each time the `<NetworkLink>` loaded into GEP
requests an update, the next point is retrieved from the list.  The update interval is set to 0.5s, but there may be 
considerably more time between points.

# Where did the flight data come from?

The flight data was downloaded from [ADSB Exchange](https://www.adsbexchange.com/data/) under their "Enthusiast Usage 
Terms".  Given the permissive nature of the usage terms, ADSB Exchange have not been formally consulted about this 
project or its usage of their data. Nonetheless, they have my thanks for making that data available.
