package edu.stonybrook.cs.wingslab.commons;
/**
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 * Representing a location in Cartesian coordination
 */

public class CartesianPoint {
    private final double x, y; // x and y coordination

    public CartesianPoint(double x, double y){
        super();
        this.x = x;
        this.y = y;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    /**
     * Adding two CartesianPoint object. Result equals: (this.x + other.x, this.y + other.y)
     * version = 1.0
     * since = 1.0
     * @param other CartesianPoint
     * @return new CartesianPoint object
     * */
    protected CartesianPoint add(CartesianPoint other){
        return new CartesianPoint(this.x + other.x, this.y + other.y);
    }

    /**
     * Subtracting other from this object. Result equals: (this.x - other.x, this.y - other.y)
     * version = 1.0
     * since = 1.0
     * @param other CartesianPoint
     * @return new CartesianPoint object
     * */
    protected CartesianPoint sub(CartesianPoint other){
        return new CartesianPoint(this.x - other.x, this.y - other.y);
    }

    /**
     * Multiplying a double number into CartesianPoint object. Result equals: (this.x * scale, this.y * scale)
     * version = 1.0
     * since = 1.0
     * @param scale CartesianPoint
     * @return new CartesianPoint object
     * */
    protected CartesianPoint mul(double scale){
        return new CartesianPoint(this.x * scale, this.y * scale);
    }
}
