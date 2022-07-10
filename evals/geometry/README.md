# Purpose

This example project is intended to demonstrate:
* Using Flask as the application+webserver for pyLiveKML
* Subclassing KML Placemarks, including:
    * Translating a simple 2D shape projected onto the xy-plane to a geospatial object (polygon) located at specific LLA coordinates
* Dynamically reconfiguring KML Placemarks, e.g. by:
    * Moving
    * Rotating
    * Re-colouring

Note that rotation and movement is shown to work for more complex shapes that have inner boundaries or cutouts.

# What does it do?

Provides a simple commandline to:
* Show or hide simple geometric shapes in GEP, initially at hard-coded LLA coordinates.
    * A ring (a circle with a concentric inner cutout) and an ellipse are provided in the example.
* Rotate either or both shapes around their centres (i.e. z-axis rotation).
    * Really only relevant for the ellipse.
* Translate (move) either or both shapes on the geoid in a specified bearing, by a specified distance.
* Change the border color of either or both shapes.
* Change the fill color of either or both shapes.

# Commandline Interface

The command and all arguments are separated by spaces.

| cmd  | description                                       |
|------|---------------------------------------------------|
| x    | exit                                              |
| load | start GEP and load the pyLiveKML interface object |
| s    | select (create) the indicated shapes in GEP       | 
| d    | deselect (delete) the indicated shapes in GEP     |
| m    | move the indicated shapes                         |
| r    | rotate the indicated shapes                       |
| c    | change colors of the indicated shapes             |
| h    | display detailed help for all commands            |
