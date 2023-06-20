package edu.stonybrook.cs.wingslab.commons;
/**
 * 2-d location
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 */
public class Point {
    private CartesianPoint cartesian;
    private PolarPoint polar;

    public Point(CartesianPoint cartesian)
    {
        super();
        this.cartesian = cartesian;
        this.polar = toPolar(cartesian);
    }

    public Point(PolarPoint polar){
        super();
        this.polar = polar;
        this.cartesian = toCartesian(polar);
    }

    public Point(double x, double y){  // Cartesian will be assumed in this case
        this(new CartesianPoint(x, y));
    }

    /**
     * A static method that convert Cartesian to Polar.
     * version = 1.0
     * since = 1.0
     * @param cartesian CartesianPoint
     * @return PolarPoint*/
    private static PolarPoint toPolar(CartesianPoint cartesian){
        double r, theta;
        r = Math.sqrt(Math.pow(cartesian.getX(), 2) + Math.pow(cartesian.getY(), 2));
        if (cartesian.getX() == 0.0)
            theta = Math.atan(Double.POSITIVE_INFINITY);
        else
            theta = Math.atan(cartesian.getY() / cartesian.getX());
        return new PolarPoint(r, theta);
    }

    /**
     * A static method that convert Polar to Cartesian.
     * version = 1.0
     * since = 1.0
     * @param polar PolarPoint
     * @return CartesianPoint*/
    private static CartesianPoint toCartesian(PolarPoint polar){
        return new CartesianPoint(polar.getR() * Math.cos(polar.getTheta()),
                polar.getR() * Math.sin(polar.getTheta()));
    }

    /**
     * Calculate distance between two CartesianPoints.
     * version = 1.0
     * since = 1.0
     * @param other Point
     * @return distance in float
     */
    public double distance(Point other) {
        return Math.sqrt(Math.pow(this.cartesian.getX() - other.cartesian.getX(), 2)
                    + Math.pow(this.cartesian.getY() - other.cartesian.getY(), 2));
    }

    /**
     * Adding two Points.
     * version = 1.0
     * since = 1.0
     * @param other Point
     * @return a new Point object
     */
    public Point add(Point other) {
        return new Point(this.cartesian.add(other.cartesian));
    }

    /**
     * Subtracting other from this object.
     * version = 1.0
     * since = 1.0
     * @param other Point
     * @return a new CartesianPoint object
     */
    public Point sub(Point other){
        return new Point(this.cartesian.sub(other.cartesian));
    }

    /**
     * Multiplying a double number into the Point.
     * version = 1.0
     * since = 1.0
     * @param scale scale that is multiplied in x and y
     * @return a new Point object
     */
    public Point mul(double scale) {
        return new Point(this.cartesian.mul(scale));
    }

    public CartesianPoint getCartesian() {
        return cartesian;
    }

    public void setCartesian(CartesianPoint cartesian) {
        this.cartesian = cartesian;
        this.polar = toPolar(cartesian);
    }

    public PolarPoint getPolar() {
        return polar;
    }

    public void setPolar(PolarPoint polar) {
        this.polar = polar;
        this.cartesian = toCartesian(polar);
    }

    /**
     * Converting Point to Geographical format point(latitude, longitude).
     * version = 1.0
     * since = 1.0
     * @param reference GeographicPoint, a reference to do conversion
     * @param point to be converted
     * @return a new Point object
     */
    public static GeographicPoint toGeographic(GeographicPoint reference, Point point){
        GeographicPoint offset = new GeographicPoint(-1.0/111111, -1.0/111111); //offset for one meter that should be added to upper_left_loc
        return new GeographicPoint(reference.getLat() + point.cartesian.getY() * offset.getLat(),
                reference.getLon() + point.cartesian.getX() * offset.getLon() /
                        Math.cos(Math.toRadians(reference.getLat() + point.cartesian.getY() * offset.getLat())));
    }

    @Override
    public String toString(){
        return String.format("%1$s,%2$s", this.cartesian.getX(), this.cartesian.getY());
    }
}
