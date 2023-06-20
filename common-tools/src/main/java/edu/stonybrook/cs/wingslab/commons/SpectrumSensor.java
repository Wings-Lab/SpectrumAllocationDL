package edu.stonybrook.cs.wingslab.commons;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.IllegalFormatException;
import java.util.Scanner;
import java.util.logging.Logger;

/**
 * Spectrum Sensor as a RX.
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 * */
public class SpectrumSensor {
    private static int ssIntId = 0;    // unique id intra SSs
    private String ssId;    // general unique id
    private RX rx;          // SS's RX
    private double cost;    // cost of using the Sensor
    private double std;     // standard deviation of the Sensor

    /** Spectrum Sensor constructor
     * @since 1.0
//     * @param ssIntId sensor id
     * @param rx sensor's receiver
     * @param cost cost of using the sensor
     * @param std standard deviation of received values*/
    public SpectrumSensor(RX rx, double cost, double std){
        super();
        this.ssId = String.format("SS%1$d", ssIntId++);
        this.rx = rx;
        this.cost = cost;
        this.std = std;
    }

    /**Copy constructor that gets a SpectrumSensor object and create a new one with equal values.*/
    public SpectrumSensor(SpectrumSensor spectrumSensor){
        super();
        this.ssId = spectrumSensor.ssId;
        this.rx = new RX(new Element(new Point(spectrumSensor.rx.getElement().getLocation().getCartesian()),
                spectrumSensor.rx.getElement().getHeight()));
        this.cost = spectrumSensor.cost;
        this.std = spectrumSensor.std;
    }

    /**reset sensor's received power*/
    public void reset(){ this.rx.setReceived_power(Double.NEGATIVE_INFINITY); }

    public String getSsId() { return ssId; }

    public RX getRx() { return rx; }

    public double getCost() { return cost; }

    public double getStd() { return std; }

    public String toString(){
        return String.format("id = %1$s", this.ssId) +
                String.format("\n%1$s", this.rx) +
                String.format("\ncost = %1$f", this.cost) +
                String.format("\nstd = %1$f", this.std);
    }

    /**Given a text path of a sensor set, this method read them and return an array of sensors.
     * The file should be in format of "x, y, height, cost, std"(with or without comma).
     * While providing x and y is mandatory, default values 1, 0, 0 will be used for height, cost, and std, respectively.
     * @param sensorFilePath file path
     * @return array of sensors
     * @since 1.0*/
    public static SpectrumSensor[] SensorReader(String sensorFilePath) throws IOException{
//        String cwd = System.getProperty("user.dir");
//        String classDir = SpectrumSensor.class.getProtectionDomain().getCodeSource().getLocation().getPath();
//        System.setProperty("user.dir", classDir);
//        System.out.println(System.getProperty("user.dir"));
        ArrayList<SpectrumSensor> sensors = new ArrayList<>();
        Path path = Paths.get(sensorFilePath);
        Scanner scanner = new Scanner(path);
        int lineNumber = 0;
        while (scanner.hasNextLine()){
            lineNumber++;
            String line = scanner.nextLine();
            String[] lines = line.split(","); // first try to use "," as decimeter
            if (lines.length < 2)
                lines = line.split(" ");  // use space decimeter if comma does not work
            double x, y;
            try {  // an exception will be raised if the line does not provide x and y location
                x = Double.parseDouble(lines[0].replaceAll(" ", ""));  // x location
                y = Double.parseDouble(lines[1].replaceAll(" ", ""));  // y location
            }
            catch (NullPointerException e){
                scanner.close();
                throw new IllegalArgumentException(String.format("File path format \"%1$s\" is not in a correct form of" +
                        " \"x, y, ...\" in line %2$d.", sensorFilePath, lineNumber));
            }
            double height = 1; // default value for height
            if (lines.length >= 3)
                height =  Double.parseDouble(lines[2].replaceAll(" ", ""));

            double cost = 0; // default value for cost
            if (lines.length >= 4)
                cost =  Double.parseDouble(lines[3].replaceAll(" ", ""));

            double std = 0; // default value for std
            if (lines.length >= 5)
                std =  Double.parseDouble(lines[4].replaceAll(" ", ""));

            sensors.add(new SpectrumSensor(
                    new RX(new Element(new Point(x, y), height)),
                    cost,
                    std));
        }
        scanner.close();
//        System.setProperty("user.dir", cwd);                    // changing back to cwd
        return sensors.toArray(new SpectrumSensor[sensors.size()]);
    }

    /**Given some parameters, this method generate a random(location) set of homogenous sensors and save them in a a file located in
     * "resources/shape_format/numberOfSensors" folder under sensors name.
     * @param numberOfSensors number of sensors to be generated
     * @param grid grid shape format
     * @param std standard deviation of reporting power values
     * @param cost cost of sensors
     * @since 1.0*/
    public static void sensorGeneratorRandom(int numberOfSensors, Shape grid, double std, double cost, double height){
        sensorGenerator(filePath(numberOfSensors, grid), grid.points(numberOfSensors), std, cost, height);
    }

    /**Given some parameters, this method generate a uniformly distributed(location) set of homogenous
     * sensors and save them in a a file located in "resources/shape_format/numberOfSensors" folder under sensors name.
     * @param numberOfSensors number of sensors to be generated
     * @param grid grid shape format
     * @param std standard deviation of reporting power values
     * @param cost cost of sensors
     * @since 1.0*/
    public static void sensorGeneratorUniform(int numberOfSensors, Shape grid, double std, double cost, double height){
        sensorGenerator(filePath(numberOfSensors, grid), grid.pointsUniform(numberOfSensors), std, cost, height);
    }

    // given number of sensors and grid shape, file name would be created
    private static String filePath(int numberOfSensors, Shape grid){
        String gridShapeFormat;
        if (grid instanceof Square square){
            gridShapeFormat = square.toString();
        }else if(grid instanceof Rectangle rect){
            gridShapeFormat = rect.toString();
        }else{
            throw new IllegalArgumentException("given grid shape" + grid.getClass().getSimpleName() +
                    "is not supported.");
        }
        return String.join("/", "resources", "sensors", gridShapeFormat,
                Integer.toString(numberOfSensors));

    }

    // general method to create sensors' information in a text file using a set of Pints
    private static void sensorGenerator(String sensorFilePath, Point[] points, double std, double cost, double height){
        Path path = Paths.get(sensorFilePath);// check if the director exists; if not, it try to create it.
        if (!Files.isDirectory(path)) {
            try {
                Files.createDirectories(path);
            }
            catch (IOException e){
                Logger logger = Logger.getLogger(SpectrumSensor.class.getName());
                logger.warning("Sensor generating operation failed due to I/O error creating directories: " +
                        Arrays.toString(e.getStackTrace()));
                return;
            }
        }

        File file = new File(sensorFilePath + "/sensors.txt");
        try (PrintWriter printLine = new PrintWriter(file)) {
            for (Point point : points)
                printLine.println(String.format("%1$s, %2$f, %3$f, %4$f", point, height, std, cost));
            printLine.flush();
            printLine.close();
            System.out.println(String.format("File %1s/sensor was successfully created.", sensorFilePath));
        } catch (FileNotFoundException e) {
            Logger logger = Logger.getLogger(SpectrumSensor.class.getName());
            logger.warning("Sensor generating operation failed due to I/O error creating the file: " +
                    Arrays.toString(e.getStackTrace()));
        }
    }
}
