package edu.stonybrook.cs.wingslab.commons;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SquareTest {

    @Test
    void TestToString() {
        Square sq1 = new Square(10);
        System.out.println(sq1);
    }
}