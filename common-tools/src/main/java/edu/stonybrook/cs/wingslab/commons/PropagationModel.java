package edu.stonybrook.cs.wingslab.commons;

/**
 * An abstract class that defines the implementation of a propagation model.
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 * */
public abstract class PropagationModel {
    public PropagationModel(){
        super();
    }
    /**
     * An abstract method that declares path loss between two location(defined as element).
     * version = 1.0
     * since = 1.0
     * @param src source element
     * @param dest destination element
     * @return path-loss value between two elements
     */
    public abstract double pathLoss(Element src, Element dest);
    /**
     * An abstract method that will be used to show useful information.
     * version = 1.0
     * since = 1.0
     * @return Information about the propagation model.
     */
    @Override
    public abstract String toString();
}
