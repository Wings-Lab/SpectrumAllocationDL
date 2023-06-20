package edu.stonybrook.cs.wingslab.commons;

import org.junit.Assert;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PointTest {

    @Test
    void distance() {
        Point p1 = new Point(new CartesianPoint(0, 9));
        Point p2 = new Point(10, 9);
        Assert.assertTrue(p1.distance(p2) == 10.0);
        Point p3 = new Point(new PolarPoint(9, Math.PI/2));
        Assert.assertTrue(p3.distance(p2) == 10.0);
    }

    @Test
    void add() {
        Point p1 = new Point(10, 9);
        Point p2 = new Point(4, 5);
        Point p3 = p1.add(p2);
        Assert.assertTrue(p3.getCartesian().getX() == 14.0);
        Assert.assertTrue(p3.getCartesian().getY() == 14.0);
    }

    @Test
    void sub() {
        Point p1 = new Point(10.2, 9);
        Point p2 = new Point(4.4, 5);
        Point p3 = p2.sub(p1);
        System.out.println(p3.getCartesian().getX());
        Assert.assertTrue(Math.round(p3.getCartesian().getX()*100.0)/100.0 == -5.8);
        Assert.assertTrue(p3.getCartesian().getY() == -4);
    }

    @Test
    void multiply() {
        Point p1 = new Point(4.3, 5.8);
        Point p2 = p1.mul(10);
        Assert.assertTrue(p2.getCartesian().getX() == 43.0);
        Assert.assertTrue(p2.getCartesian().getY() == 58.0);

    }

    @Test
    void setCartesian() {
        Point p1 = new Point(4.3, 5.8);
        System.out.println(p1.getPolar().getR() + "," + p1.getPolar().getTheta());
        p1.setCartesian(new CartesianPoint(5.6, 4.2));
        System.out.println(p1.getPolar().getR() + "," + p1.getPolar().getTheta());
    }

    @Test
    void setPolar() {
        Point p1 = new Point(new PolarPoint(10, 0));
        System.out.println(p1.getCartesian().getX() + "," + p1.getCartesian().getY());
        p1.setPolar(new PolarPoint(5.6, 4.2));
        System.out.println(p1.getCartesian().getX() + "," + p1.getCartesian().getY());
    }

    @Test
    void toGeographic() {
        GeographicPoint p1 = Point.toGeographic(new GeographicPoint(40.800595, 73.107507),
                new Point(100, 50));
        System.out.println(p1.getLat() + "," + p1.getLon());
    }

    @Test
    void testToString() {
        Point p1 = new Point(new PolarPoint(10, 0));
        Assert.assertTrue(p1.toString().equals("10.0,0.0"));
    }
}