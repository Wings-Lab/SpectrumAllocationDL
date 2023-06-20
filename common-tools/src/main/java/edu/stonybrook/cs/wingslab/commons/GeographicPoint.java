package edu.stonybrook.cs.wingslab.commons;
/**
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 * Representing a location with latitude and longitude.
 */
public class GeographicPoint {
    private final double lat, lon;

    public GeographicPoint(double lat, double lon) {
        this.lat = lat;
        this.lon = lon;
    }

    public double getLat() {
        return lat;
    }

    public double getLon() {
        return lon;
    }
}
