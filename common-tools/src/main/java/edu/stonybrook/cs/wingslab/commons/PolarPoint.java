package edu.stonybrook.cs.wingslab.commons;


/**
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 * Representing a location in polar coordination
 */
public class PolarPoint {
    private final double r;
    private final double theta;

    public PolarPoint(double r, double theta){
        super();
        this.r = r;
        this.theta = theta;
    }

    public double getR() {
        return r;
    }

    public double getTheta() {
        return theta;
    }
}
