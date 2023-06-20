package edu.stonybrook.cs.wingslab.commons;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class RectangleTest {

    @Test
    void points() {
        Rectangle rect1 = new Rectangle(10, 2);
        for (Point p:rect1.points(30))
            System.out.println(p);
    }

    @Test
    void all_points() {
        Rectangle rect1 = new Rectangle(10, 3);
        for (Point p:rect1.allPoints())
            System.out.println(p);
    }

    @Test
    void testToString() {
        Rectangle rect1 = new Rectangle(10, 3);
        System.out.println(rect1);
    }

    @Test
    void pointsUniform() {
        Rectangle rect1 = new Rectangle(100, 100);
        for (int i = 0; i < 1000; i++)
            rect1.pointsUniform(i);
    }
}