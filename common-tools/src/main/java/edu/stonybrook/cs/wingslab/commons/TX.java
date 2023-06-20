package edu.stonybrook.cs.wingslab.commons;

/**
 * Transmitter with a location and a sending power.
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 */
public class TX {
    private Element element;
    private double power;  // power sent in dB

    public TX(Element element, double power){
        this.element = element;
        this.power = power;
    }

    public Element getElement() {
        return element;
    }

    public void setElement(Element element) {
        this.element = element;
    }

    public double getPower() {
        return power;
    }

    public void setPower(double power) {
        this.power = power;
    }

    @Override
    public String toString(){
        return String.format("TX\n%1$s\n%2$.3f", element, power);
    }
}
