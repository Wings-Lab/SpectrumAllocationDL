package edu.stonybrook.cs.wingslab.commons;

import java.util.Arrays;
import java.util.Comparator;

/**
 * Unreal Spectrum Sensor list generated from real sensors. Their power value obtained with interpolation
 * based on number of sensors to be selected.
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 * */
public class InterpolatedSpectrumSensor {
    /** Type of interpolation*/
    public enum InterpolationType{
        /**Interpolation based on log(distance)*/
        LOG,    // based on log of distances
        /**Interpolation based on distance*/
        LINEAR, // based on distances
    }

    class SensorDistance{  // used to calculated nearest sensors
        SpectrumSensor sensor;
        double distance;
        SensorDistance(SpectrumSensor sensor, double distance){
            this.sensor = sensor;
            this.distance = distance;
        }

        public double getDistance() {
            return distance;
        }

        public SpectrumSensor getSensor(){
            return sensor;
        }
    }
    private final SpectrumSensor[] sss;                  // list of real SpectrumSensor
    private final SpectrumSensor[] interSss;             // list of interpolated sss

    /**InterpolatedSpectrumSensor constructor. Given the list of sensors power values of the new list are interpolated.
     * @param sss the list of sensors with known power values
     * @param interSss the list of sensors whose power values are interpolated
     * @param interpolationType IDW type either Log(distance) or distance
     * @param numberOfInterpolatedSensor number of known sensors to use for interpolation*/
    public InterpolatedSpectrumSensor(SpectrumSensor[] sss, SpectrumSensor[] interSss,
                                      InterpolationType interpolationType, int numberOfInterpolatedSensor){
        this.sss = sss;
        // number od interpolated sensors
        this.interSss = interSss;
        // reset power for interpolated sensors
        for (SpectrumSensor ss : this.interSss)
            ss.reset();

        for (SpectrumSensor iss : this.interSss) {  // O(#interSss)
            SensorDistance[] ssd = new SensorDistance[this.sss.length];     // arrays of sensors with distance to iss
            for (int i = 0; i < this.sss.length; i++)   //O(#ss)
                ssd[i] = new SensorDistance(this.sss[i],
                        this.sss[i].getRx().getElement().getLocation().distance(
                                iss.getRx().getElement().getLocation()));
            Arrays.sort(ssd, Comparator.comparing(SensorDistance::getDistance));    //O(#sslog(#ss))
            double totalInverseWeight = 0.0;        // calculate total weight
            for (int w = 0; w < numberOfInterpolatedSensor; w++)
                totalInverseWeight += switch (interpolationType){
                    case LINEAR: yield ssd[w].getDistance();
                    case LOG: yield Math.log10(ssd[w].getDistance());
                };
            //calculating interpolated value
            double interPower = 0.0;
            for (int w = 0; w < numberOfInterpolatedSensor; w++){
                double weight = switch (interpolationType){
                    case LINEAR: yield ssd[w].getDistance();
                    case LOG: yield Math.log10(ssd[w].getDistance());
                };
                interPower += ssd[w].getSensor().getRx().getReceived_power() / weight / 1 / totalInverseWeight;
            }
            iss.getRx().setReceived_power(interPower);
        }
    }

    /**@return new interpolated list of sensors*/
    public SpectrumSensor[] getInterSss(){ return this.interSss; }

    /**@return String of interpolated sensors list including location and power*/
    @Override
    public String toString() {
        // sensors information
        StringBuilder ssInformation = new StringBuilder(""); // better to use StringBuilder for concatenation
        for (int ss = 0; ss < this.interSss.length - 1; ss++)
            ssInformation.append(String.format("%.3f,", this.interSss[ss].getRx().getReceived_power()));
        ssInformation.append(String.format("%.3f",
                this.interSss[this.interSss.length - 1].getRx().getReceived_power()));
        return ssInformation.toString();
    }
}
