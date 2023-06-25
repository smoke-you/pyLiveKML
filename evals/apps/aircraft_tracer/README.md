# Purpose

This example app is intended to demonstrate:
* Subclassing KML Placemarks to incorporate additional fields
* Constraining the rate at which data is loaded into GEP

# What Does it Do?
Tracking information from several (up to three) commercial flights is displayed in GEP as Placemarks under individual 
Folders, one Folder per aircraft.  All the Placemarks for the selected flights will, over time, be displayed in GEP. 
Data is loaded over time to avoid the perceptible refresh delay that would occur if circa 6000 Placemarks were created 
in a single Update tag.

# Where did the flight data come from?

The flight data was downloaded from [ADSB Exchange](https://www.adsbexchange.com/data/) under their "Enthusiast Usage 
Terms".  Given the permissive nature of the usage terms, ADSB Exchange have not been formally consulted about this 
project or its usage of their data. Nonetheless, they have my thanks for making that data available.
