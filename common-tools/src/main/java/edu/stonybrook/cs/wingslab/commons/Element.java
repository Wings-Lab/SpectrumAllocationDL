package edu.stonybrook.cs.wingslab.commons;

/**
 * A wrapper class for representing location(including height) of all elements
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0*/
public class Element {
    private Point location;
    private double height;

    public Element(Point point, double height){
        super();
        this.location = point;
        this.height = height;
    }

    public Point getLocation() {
        return location;
    }

    public void setLocation(Point location) {
        this.location = location;
    }

    public double getHeight() {
        return height;
    }

    public void setHeight(double height) {
        this.height = height;
    }

    /**
     * Adding a Point to the element.
     * version = 1.0
     * since = 1.0
     * @param other Point
     * @return a new Element object
     */
    public Element add(Point other) {
        return new Element(this.location.add(other), this.height);
    }

    /**
     * Subtracting other Point from the element's location.
     * version = 1.0
     * since = 1.0
     * @param other Point
     * @return a new Element object
     */
    public Element sub(Point other){
        return new Element(this.location.sub(other), this.height);
    }

    /**
     * Multiplying a double number into a the element's location.
     * version = 1.0
     * since = 1.0
     * @param scale a double value multiplied by the location
     * @return a new Element object
     */
    public Element mul(double scale) {
        return new Element(this.location.mul(scale), this.height);
    }

    @Override
    public String toString(){
        return String.format("location=%1$s\nheight=%2$s", this.location, this.height);
    }
}
