package edu.stonybrook.cs.wingslab.commons;

import org.junit.Assert;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class WirelessToolsTest {

    @Test
    void getDecimal() {
        System.out.println(WirelessTools.getDB(5));
        System.out.println(WirelessTools.getDecimal(WirelessTools.getDB(5)));
        Assert.assertTrue(5.0 == WirelessTools.getDecimal(WirelessTools.getDB(5)));
    }
}