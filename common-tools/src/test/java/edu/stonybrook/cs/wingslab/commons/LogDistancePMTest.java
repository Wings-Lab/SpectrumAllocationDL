package edu.stonybrook.cs.wingslab.commons;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class LogDistancePMTest {

    @Test
    void pathLoss() {
        LogDistancePM log1 = new LogDistancePM(3);
        double[] distances = new double[]{1, 5, 10, 15, 20, 50, 100, 1000};
        for (double distance : distances)
            System.out.println(distance + ": " + log1.pathLoss(new Element(new Point(0, 0), 10),
                    new Element(new Point(distance, 0), 10)));
    }

    @Test
    void pathLoss2(){
        LogDistancePM log1 = new LogDistancePM(3, 1);
        int iter = 3000;
        double sum = 0.0;
        for (int i = 0; i < iter; i++) {
            double pl = log1.pathLoss(new Element(new Point(0, 0), 10),
                    new Element(new Point(10, 0), 10));
            sum += pl;
//            System.out.println(pl);
        }
        System.out.println("mean= " + sum/iter);
    }

    @Test
    void pathLoss3(){
        LogDistancePM log1 = new LogDistancePM(3, 5, 10.0);
        double[] distances = new double[]{1, 5, 10, 15, 20, 50, 100, 1000};
        for (double distance : distances)
            System.out.println(distance + ": " + log1.pathLoss(new Element(new Point(0, 0), 10),
                    new Element(new Point(distance, 0), 10)));
    }

    @Test
    void pathLoss4(){
        LogDistancePM log1 = new LogDistancePM(3, 0.0 ,0.0, 0.0, 0.0, 0.5);
        double[] distances = new double[]{0.5, 1, 5, 10, 15, 20, 50, 100, 1000};
        for (double distance : distances)
            System.out.println(distance + ": " + log1.pathLoss(new Element(new Point(0, 0), 10),
                    new Element(new Point(distance, 0), 10)));
    }

    @Test
    void testToString() {
        LogDistancePM log1 = new LogDistancePM(3);
        System.out.println(log1);
        LogDistancePM log2 = new LogDistancePM(3, 1.0);
        System.out.println(log2);
    }
}