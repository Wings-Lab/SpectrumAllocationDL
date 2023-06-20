package edu.stonybrook.cs.wingslab.commons;

/**
 * Receiver with a location and a received power.
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 */
public class RX {
    private Element element;
    private double received_power;

    public RX(Element element){
        this.element = element;
        this.received_power = Double.NEGATIVE_INFINITY;
    }

    public Element getElement() {
        return element;
    }

    public void setElement(Element element) {
        this.element = element;
    }

    public double getReceived_power() {
        return received_power;
    }

    public void setReceived_power(double received_power) {
        this.received_power = received_power;
    }

    @Override
    public String toString(){
        return String.format("RX:{%1$s\nreceived power = %2$.3f}", element, received_power);
    }
}
