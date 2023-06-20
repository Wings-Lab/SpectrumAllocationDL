package edu.stonybrook.cs.wingslab.commons;

import java.util.concurrent.ThreadLocalRandom;
import java.util.logging.Logger;

/**
 * Rectangle shape.
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 */
public class Rectangle extends Shape{
    private final int width, length;

    /**Copy constructor
     * @param rectangle Rectangle object*/
    public Rectangle(Rectangle rectangle){
        super();
        this.width = rectangle.width;
        this.length = rectangle.length;
    }

    /**
     * Create Rectangle object given length and width originated in Point(0, 0)*/
    public Rectangle(int width, int length){
        super();
        this.width = width;
        this.length = length;
    }

    /**
     * Given number of points, n, this method return n random Points inside the rectangle.
     * version = 1.0
     * since = 1.0
     * @param n number of points
     * @return An array of n Points
     */
    @Override
    public Point[] points(int n) {
        if (n > width * length) {
            Logger logger = Logger.getLogger(Rectangle.class.getName());
            logger.warning("Number of requested Points is more than all the points. Duplicates exist.");
        }
        Point[] points = new Point[n];
        for (int i = 0; i < n; i++)
            points[i] = new Point(ThreadLocalRandom.current().nextInt(0, width),
                    ThreadLocalRandom.current().nextInt(0, length));
        return points;
    }

    /**
     * Given number of points, n, this method return n Points (most possible) uniformly distributed inside the shape.
     * version = 1.0
     * since = 1.0
     *
     * @param n number of points
     * @return An array of n Points
     */
    @Override
    public Point[] pointsUniform(int n) {
        Point[] points = new Point[n];
        int area = width * length;
        int modified_n = n;
        if (length == width)
            modified_n = (int)Math.sqrt(n) * (int)Math.sqrt(n);
        double pointCoverage = (double) area / modified_n;  // area covered by each point
        double x_dist = Math.sqrt(pointCoverage) * (double) (width / length);
        // width of pointCoverage; distance between two points in x(width) ax
        double y_dist = Math.sqrt(pointCoverage) * (double) (length / width);
        // length of pointCoverage; distance between two points in y(width) ax

        int x_num = (int) (100000 * width / x_dist) / 100000;  // number of points in each row(x-ax)
        int y_num = (int) (100000 * length / y_dist) / 100000; //number of points in each row(x-ax)

        double[] x_indexes = new double[x_num + 1];
        for (int x = 0; x <= x_num; x++)
            x_indexes[x] = x * x_dist;
        double[] y_indexes = new double[y_num + 1];
        for (int y = 0; y <= y_num; y++)
            y_indexes[y] = y * y_dist;

        int[] point_x_indexes = new int[x_num];
        for (int x = 0; x < x_num; x++)
            point_x_indexes[x] = Math.min((int)((x_indexes[x] + x_indexes[x + 1]) / 2), width - 1);
        int[] point_y_indexes = new int[y_num];
        for (int y = 0; y < y_num; y++)
            point_y_indexes[y] = Math.min((int)((y_indexes[y] + y_indexes[y + 1]) / 2), length - 1);

        int point_cnt = 0;
        for (int x : point_x_indexes)
            for (int y : point_y_indexes)
                points[point_cnt++] = new Point(x, y);

        // because of double to int conversion, above algorithm might not create enough points;
        // the rest would be created randomly
        while (point_cnt < n)
            points[point_cnt++] = new Point(ThreadLocalRandom.current().nextInt(0, width),
                    ThreadLocalRandom.current().nextInt(0, length));
        return points;
    }

    public int getWidth() {
        return width;
    }

    public int getLength() {
        return length;
    }

    /**
     * This method return all Points inside the rectangle.
     * version = 1.0
     * since = 1.0
     *
     * @return An array of all Points
     */
    @Override
    public Point[] allPoints() {
        Point[] points = new Point[width * length];
        for (int x = 0; x < width; x++)
            for (int y = 0; y < length; y++)
                points[x * length + y] = new Point(x, y);
        return points;
    }

    @Override
    public String toString() {
        return String.format("%1$s%2$s_%3$s", Rectangle.class.getSimpleName().toLowerCase(), width, length);
    }
}
