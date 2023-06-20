package edu.stonybrook.cs.wingslab.commons;
/**
 * An abstract class that defines the shape of the target field
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 * */
public abstract class Shape {
    /**
     * Given number of points, n, this method return n random Points inside the shape.
     * version = 1.0
     * since = 1.0
     * @param n number of points
     * @return An array of n Points
     */
    public abstract Point[] points(int n);

    /**
     * Given number of points, n, this method return n Points (most possible) uniformly distributed inside the shape.
     * version = 1.0
     * since = 1.0
     * @param n number of points
     * @return An array of n Points
     */
    public abstract Point[] pointsUniform(int n);

    /**
     * This method return all Points inside the shape.
     * version = 1.0
     * since = 1.0
     * @return An array of all Points
     */
    public abstract Point[] allPoints();

    @Override
    public abstract String toString();
}
