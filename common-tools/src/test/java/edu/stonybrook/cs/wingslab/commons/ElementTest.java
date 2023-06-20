package edu.stonybrook.cs.wingslab.commons;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ElementTest {

    @Test
    void testToString() {
        Element e1 = new Element(new Point(10, 4), 13);
        System.out.println(e1);
    }
}