package edu.stonybrook.cs.wingslab.commons;

import java.util.Random;

/**
 * Immutable Log-Distance(Normal) propagation model with path loss coefficient alpha and a sinus wave equivalent to
 * shadowing with a period and amplitude. Multi-path effect is considered as a noise with a standard deviation if noise
 * is allowed.
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 * */
public class LogDistancePM extends PropagationModel{
    private final double alpha;  // path-loss coefficient pl = 10*alpha*log10(distance)
    private final boolean multiPathNoise;  // if multi-path is enabled. False if multiPathStd not provided
    private final double multiPathStd;  // a gaussian noise with zero mean and multiPathStd standard deviation
    private final boolean shadow;  // if shadowing is enabled. False if shadowAmp/shadowPeriod not provided
    private final double shadowAmp;  // amplitude of shadowing sinus wave
    private final double shadowPeriod;  // period of shadowing sinus wave
    private final double plReference;  // path-loss reference at dist_ref. 0.0 if not provided
    private final double distReference; // reference distance where path-loss is plReference. 1.0 if not provided
    private final Random gauss;

    /**Copy constructor.
     * @param logDistancePM LogDistancePM object*/
    public LogDistancePM(LogDistancePM logDistancePM){
        super();
        this.alpha = logDistancePM.alpha;
        this.multiPathNoise = logDistancePM.multiPathNoise;
        this.multiPathStd = logDistancePM.multiPathStd;
        this.shadow = logDistancePM.shadow;
        this.shadowAmp = logDistancePM.shadowAmp;
        this.shadowPeriod = logDistancePM.shadowPeriod;
        this.plReference = logDistancePM.plReference;
        this.distReference = logDistancePM.distReference;
        this.gauss = new Random();
    }

    /**
     * General log-distance constructor with shadowing and multi-path effects.
     * version = 1.0
     * since = 1.0
     * @param alpha  path-loss coefficient
     * @param multiPathNoise enable/disable multi-path effect
     * @param multiPathStd Standard deviation of multi-path effect as a zero-mean Gaussian noise.
     * @param shadow enable/disable shadowing
     * @param shadowAmp amplitude of sinus-wave shadowing
     * @param shadowPeriod period of sinus-wave shadowing
     */
    private LogDistancePM(double alpha, boolean multiPathNoise, double multiPathStd,
                          boolean shadow, double shadowAmp, double shadowPeriod,
                          double plReference, double distReference){
        super();
        this.alpha = alpha;
        this.multiPathNoise = multiPathNoise;
        this.multiPathStd = multiPathStd;
        this.shadow = shadow;
        this.shadowAmp = shadowAmp;
        this.shadowPeriod = shadowPeriod;
        this.plReference = plReference;
        this.distReference = distReference;
        this.gauss = new Random();
    }

    /**
     * Log-distance constructor with shadowing and multi-path effects. path-loss reference=0 and distance reference=1
     * version = 1.0
     * since = 1.0
     * @param alpha  path-loss coefficient
     * @param multiPathStd Standard deviation of multi-path effect as a zero-mean Gaussian noise.
     * @param shadowAmp amplitude of sinus-wave shadowing
     * @param shadowPeriod period of sinus-wave shadowing
     */
    public LogDistancePM(double alpha, double multiPathStd, double shadowAmp, double shadowPeriod){
        this(alpha, true, multiPathStd, true, shadowAmp, shadowPeriod,
                0.0, 1.0);
    }

    /**
     * Log-distance constructor with shadowing and multi-path effects.
     * version = 1.0
     * since = 1.0
     * @param alpha  path-loss coefficient
     * @param multiPathStd Standard deviation of multi-path effect as a zero-mean Gaussian noise.
     * @param shadowAmp amplitude of sinus-wave shadowing
     * @param shadowPeriod period of sinus-wave shadowing
     * @param plReference path-loss reference
     * @param distReference distance reference
     */
    public LogDistancePM(double alpha, double multiPathStd, double shadowAmp, double shadowPeriod,
                         double plReference, double distReference){
        this(alpha, true, multiPathStd, true, shadowAmp, shadowPeriod,
                plReference, distReference);
    }

    /**
     * Log-distance constructor with multi-path effect only. path-loss reference=0 and distance reference=1
     * version = 1.0
     * since = 1.0
     * @param alpha  path-loss coefficient
     * @param multiPathStd Standard deviation of multi-path effect as a zero-mean Gaussian noise.
     */
    public LogDistancePM(double alpha, double multiPathStd){
        this(alpha, true, multiPathStd, false, 0.0, 0.0,
                0.0, 1.0);
    }

    /**
     * Log-distance constructor with shadowing effect only.
     * version = 1.0
     * since = 1.0
     * @param alpha  path-loss coefficient
     * @param shadowAmp amplitude of sinus-wave shadowing
     * @param shadowPeriod period of sinus-wave shadowing
     */
    public LogDistancePM(double alpha, double shadowAmp, double shadowPeriod){
        this(alpha, false, 0.0, true, shadowAmp, shadowPeriod,
                0.0, 1.0);
    }

    /**
     * Log-distance constructor without multi-path or shadowing effect. path-loss reference=0 and distance reference=1
     * version = 1.0
     * since = 1.0
     * @param alpha  path-loss coefficient
     */
    public LogDistancePM(double alpha){
        this(alpha, false, 0.0, false, 0.0, 0.0,
                0.0, 1.0);
    }

    /**
     * Method that returns path-loss between two location(defined as element) based on Log-Distance Propagation model.
     * version = 1.0
     * since = 1.0
     * @param src  source element
     * @param dest destination element
     * @return Log-distance path-loss value between two elements
     */
    @Override
    public double pathLoss(Element src, Element dest) {
        double distance = src.getLocation().distance(dest.getLocation()) / this.distReference;
        double loss = this.plReference;
        if (distance > 1.0) {
            loss += 10 * this.alpha * Math.log10(distance); // add distance-based loss
            if (this.shadow) // add shadowing
                loss += this.shadowAmp * Math.sin(2 * Math.PI * Math.log10(distance) / Math.log10(this.shadowPeriod));
        }
        if (this.multiPathNoise) // add zero-mean multi-path gaussian noise
            loss += this.gauss.nextGaussian() * this.multiPathStd;
        return loss;
    }

    public double getAlpha() { return alpha; }

    public boolean isMultiPathNoise() { return multiPathNoise; }

    public double getMultiPathStd() { return multiPathStd; }

    public boolean isShadow() { return shadow; }

    public double getShadowAmp() { return shadowAmp; }

    public double getShadowPeriod() { return shadowPeriod; }

    public double getPlReference() { return plReference; }

    public double getDistReference() { return distReference; }

    /**
     * An abstract method that will be used to show useful information.
     * version = 1.0
     * since = 1.0
     *
     * @return Information about the propagation model.
     */
    @Override
    public String toString() {
        String noise_msg = this.multiPathNoise ? String.format("std= %1$.2f", this.multiPathStd) : "";
        return String.format("Log-Distance(Normal):\n" +
                "Path-Loss Coeff.= %1$.2f\n" +
                "Path-Loss reference %2$.2fdB in distance reference %3$.2fm\n" +
                noise_msg, this.alpha, this.plReference, this.distReference);
    }
}
