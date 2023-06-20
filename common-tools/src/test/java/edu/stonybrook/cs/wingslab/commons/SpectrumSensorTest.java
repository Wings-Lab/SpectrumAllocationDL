package edu.stonybrook.cs.wingslab.commons;

import org.junit.Assert;
import org.junit.jupiter.api.Test;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

class SpectrumSensorTest {

    @Test
    void testToString() {
        SpectrumSensor ss1 = new SpectrumSensor( new RX(new Element(new Point(1, 1),
                10)), 1.0, 1);
        System.out.println(ss1);
    }

    @Test
    void sensorGeneratorRandom() {
        SpectrumSensor.sensorGeneratorRandom(400, new Square(1000), 0.732, 1.0, 15);
    }

    @Test
    void sensorGeneratorUniform() {
        SpectrumSensor.sensorGeneratorUniform(1600, new Square(1000), 0.732, 1.0, 15);
    }

    @Test
    public void testSensorReader() throws IOException {
        SpectrumSensor[] sensors = SpectrumSensor.SensorReader("resources/sensors/square1000/1600/sensors.txt");
        Assert.assertTrue(sensors.length == 900);
    }

    @Test
    void testCopyConstructor(){
        SpectrumSensor ss1 = new SpectrumSensor( new RX(new Element(new Point(1, 1),
                10)), 1.0, 1);
        SpectrumSensor ss2 = new SpectrumSensor(ss1);
        Assert.assertNotSame(ss1, ss2);
        Assert.assertNotSame(ss1.getRx(), ss2.getRx());
        System.out.println(ss1);
        System.out.println(ss2);
    }
}