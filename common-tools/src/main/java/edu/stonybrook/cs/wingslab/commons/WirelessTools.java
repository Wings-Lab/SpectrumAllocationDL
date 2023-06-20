package edu.stonybrook.cs.wingslab.commons;

/**
 * Useful static methods in Wireless area. This class can't be instantiated.
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 * Representing a location in Cartesian coordination
 */
public final class WirelessTools {
    private WirelessTools(){} // can't be instantiated.
    /**
     * Given a decibel(or mili decibel) value, this method return its decimal.
     * version = 1.0
     * since = 1.0
     * @param dbValue decibel value
     * @return Decimal value
     */
    public static double getDecimal(double dbValue){ return Math.pow(10, dbValue/10);}
    /**
     * Given a decimal value, this method returns ots decibel value.
     * version = 1.0
     * since = 1.0
     * @param decimalValue decimal value
     * @return (mili) decibel value
     */
    public static double getDB(double decimalValue){
        if (decimalValue <= 0)
            return Double.NEGATIVE_INFINITY;
        return 10 * Math.log10(decimalValue);
    }
}
