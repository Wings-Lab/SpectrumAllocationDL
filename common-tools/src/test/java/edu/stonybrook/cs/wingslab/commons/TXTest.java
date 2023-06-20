package edu.stonybrook.cs.wingslab.commons;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TXTest {

    @Test
    void testToString() {
        TX tx1 = new TX(new Element(new Point(10, 5), 15), 8.435673);
        System.out.println(tx1);
    }
}