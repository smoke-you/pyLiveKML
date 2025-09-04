# Purpose

This example app is intended to demonstrate:

* Subclassing KML Placemarks, including:

    * Transforming a simple 2D shape projected onto the xy-plane into a geospatial object (polygon) located at specific LLA coordinates

* Dynamically reconfiguring KML Polygons, e.g. by:

    * Translation in latitude, longitude and/or altitude

    * Rotation around an origin

    * Re-colouring

Note that rotation and translation is shown to work for more complex shapes that have inner boundaries or cutouts.
