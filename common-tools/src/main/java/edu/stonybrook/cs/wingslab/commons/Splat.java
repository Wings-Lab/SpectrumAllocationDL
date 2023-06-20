package edu.stonybrook.cs.wingslab.commons;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.lang.reflect.Type;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ThreadLocalRandom;
import java.util.logging.Logger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * SPLAT! site type used for file's name that is being created*/
enum SiteType{
    TX,
    RX
}
/**
 * Splat! site stands for either a transmitter or receiver.
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 * */
final class SplatSite{
    private final String name;
    private final GeographicPoint point;
    private final double height;
    private final SiteType type;

    /**SplatSite constructor.
     * @param type TX/RX
     * @param point Geographic point(lat, lon)
     * @param height height of the element*/
    SplatSite(SiteType type, GeographicPoint point, double height){
        super();
        this.point = point;
        this.type = type;
        this.height = height;
        String tp = switch (type){
            case RX -> "rx";
            case TX -> "tx";
            default -> throw new IllegalArgumentException("Wrong site type " + type);
        };
        this.name = String.format("%1$s-N%2$dW%3$d-%4$d",
                tp,
                Math.abs((int)point.getLat() * 1000),
                Math.abs((int)point.getLon() * 1000),
                ThreadLocalRandom.current().nextInt(0, 100000000));

    }

    String getName() {
        return name;
    }

    GeographicPoint getPoint() {
        return point;
    }

    double getHeight() {
        return height;
    }

    SiteType getType() {
        return type;
    }

    /**Create a qth file used by SPLAT! simulator.*/
    String CreateQTHFile(String path){
        Path filePath = Paths.get(path);// check if the director exists; if not, it try to create it.
        if (!Files.isDirectory(filePath)) {
            try {
                Files.createDirectories(filePath);
            }
            catch (IOException e){
                Logger logger = Logger.getLogger(SpectrumSensor.class.getName());
                logger.warning("Sensor generating operation failed due to I/O error creating directories: " +
                        Arrays.toString(e.getStackTrace()));
                return "";
            }
        }

        File file = new File(filePath + "/" + this.name + ".qth");
        try (PrintWriter printLine = new PrintWriter(file)) {
            printLine.print(this);
            printLine.flush();
        } catch (FileNotFoundException e) {
            Logger logger = Logger.getLogger(SpectrumSensor.class.getName());
            logger.warning("Sensor generating operation failed due to I/O error creating the file: " +
                    Arrays.toString(e.getStackTrace()));
            return "";
        }
        return this.name;
    }

    public String toString(){
        return String.format("%1$s\n%2$f\n%3$f\n%4$f", this.name, Math.abs(this.point.getLat()),
                Math.abs(this.point.getLon()),
                this.height);
    }

}

/**
 * A wrapper class for Splat! propagation model (simulator) that executes a command in Linux/Unix. Should be already installed.
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 * */
public class Splat extends PropagationModel{
    private static String SDF_DIR = "resources/splat/sdf";    //path where sdf files are located
    private static final GeographicPoint OFFSET =
            new GeographicPoint(-1.0/111111, -1.0/111111);  // offset for one meter that should be added
                                                                    // to upper_left_loc
    private static final long TIMEOUT = 200;                      // time-out(milliseconds) for the simulator to finish the calculations
    private static final int APPROX = 10;                           // SPLAT! will not be used if there is a previous
                                                                    // saved path loss in vicinity of APPROX meter
    private static final String SPLAT_COMMAND = "splat";            // 'splat' or 'splat-hd'
    private static ConcurrentHashMap<String,
            ConcurrentHashMap<String, Double>> plDict;            // hash dictionary for path-loss values

    private final GeographicPoint reference;                                    //upper left corner of the field
    private long fetchTime = 0;
    private long fetchNum = 0;
    private long execTime = 0;
    private long execNum = 0;

    /**Splat constructor
     * @param reference left-upper GeographicPoint reference*/
    public Splat(GeographicPoint reference){
        super();
        this.reference = reference;
    }

    /**Copy constructor
     * @param splat Splat object*/
    public Splat(Splat splat){
        super();
        this.reference = splat.getReference();
    }

    /**
     * SPLAT! path-loss calculations method that receives two location(defined as element).
     * version = 1.0
     * since = 1.0
     *
     * @param src  source element
     * @param dest destination element
     * @return path-loss value between two elements
     */
    @Override
    public double pathLoss(Element src, Element dest) {
        return pathLoss(src, dest, 0);
    }

    private double pathLoss(Element src, Element dest, int iteration) {
        if (iteration == 10)
            throw new RuntimeException("Path-loss cannot be calculated");
        double tmpFetchTime = System.currentTimeMillis();
        // convert given Point to its nearest approximated value defined by APPROX
        int approxSrcX = ((int) (src.getLocation().getCartesian().getX() / Splat.APPROX)) * Splat.APPROX;
        int approxSrcY = ((int) (src.getLocation().getCartesian().getY() / Splat.APPROX)) * Splat.APPROX;
        int approxDestX = ((int) (dest.getLocation().getCartesian().getX() / Splat.APPROX)) * Splat.APPROX;
        int approxDestY = ((int) (dest.getLocation().getCartesian().getY() / Splat.APPROX)) * Splat.APPROX;
        String srcKey = String.format("%04d%04d",approxSrcX, approxSrcY);      // tx key
        String destKey = String.format("%04d%04d",approxDestX, approxDestY);      // rx key
        // check if a pl values exists for both keys
        if (Splat.plDict.containsKey(srcKey) && Splat.plDict.get(srcKey).containsKey(destKey)) {
            double plValue = Splat.plDict.get(srcKey).get(destKey);
            this.fetchNum++;
            this.fetchTime += System.currentTimeMillis() - tmpFetchTime;
            return plValue;
        }
        // execute SPLAT! command because there is no path-loss value for the above keys
        double tmpExecTime = System.currentTimeMillis();
        String pwd = Paths.get(".").toAbsolutePath().toString();  // get current directory

        //executing splat command
        int count = 0;
        Process proc = null;
        String srcName = null;
        String destName = null;

        double startTime = System.currentTimeMillis();  // will be used to check how long simulating takes

        while (true) {
            if (proc!= null && !proc.isAlive())
                break;
            else {
                if (proc == null || (System.currentTimeMillis() - startTime) > Splat.TIMEOUT) {
                    if (proc != null)
                        proc.destroy();
                    double offset = count / 10.0;

                    // adding a small values to src and dest locations might help
                    GeographicPoint srcLoc = Point.toGeographic(this.reference,
                            src.getLocation().add(new Point(Splat.random(offset), Splat.random(offset))));
                    GeographicPoint destLoc = Point.toGeographic(this.reference,
                            dest.getLocation().add(new Point(Splat.random(offset), Splat.random(offset))));

                    //create QTH files
                    srcName = new SplatSite(SiteType.TX, srcLoc, src.getHeight()).CreateQTHFile(Splat.SDF_DIR);
                    destName = new SplatSite(SiteType.RX, destLoc, dest.getHeight()).CreateQTHFile(Splat.SDF_DIR);

                    String command = String.format("%1$s -t %2$s.qth -r %3$s.qth", SPLAT_COMMAND, srcName, destName);

                    try {
                        proc = Runtime.getRuntime().exec(command, null, new File(SDF_DIR));
                    } catch (IOException e) {
                        System.out.println("Error happened executing SPLAT! command.\n" +
                                Arrays.toString(e.getStackTrace()));
                    }
                    count++;
                    startTime = System.currentTimeMillis();
                }
                else {
                    try {
                        Thread.sleep(Splat.TIMEOUT / 5);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }

        String outputName = String.format("%1$s-to-%2$s.txt", srcName, destName);
        double pathLossValue;
        try {
            pathLossValue =  processOutput(outputName);
        } catch (IOException e) {
            System.out.println("Warning: Recalling is happening");
            return this.pathLoss(src, dest, iteration++);
        }finally {
            //deleting text files generated by splat
            Splat.deleteTextFiles(outputName, srcName, destName);
        }

        if (!Splat.plDict.containsKey(srcKey)) // src key not existed
            Splat.plDict.put(srcKey, new ConcurrentHashMap<>());
        Splat.plDict.get(srcKey).put(destKey, pathLossValue);

        this.execNum++;
        this.execTime += System.currentTimeMillis() - tmpExecTime;  // add seconds to the whole running time
        return pathLossValue;
    }

    // return a random value [-offset, offset]
    private static double random(double offset){
        return offset * (-1 + 2 * Math.random());
    }

    //method to process the output generated by SPLAT! to get path-loss values
    public static double processOutput(String fileName) throws IOException {
//        String positiveFloat = "([0-9]*[.])?[0-9]+";
//        String positiveFloat = "^\\D+(\\d+).*";
        String positiveFloat = "(\\d+\\.\\d+)";
        String freeSpacePatternStr = String.format("Free space.*\\D%1$s.*", positiveFloat);
        String itmPatternStr = String.format("ITWOM Version 3.0.*\\D%1$s.*", positiveFloat);

        Pattern freePattern = Pattern.compile(freeSpacePatternStr);
        Pattern itmPattern = Pattern.compile(itmPatternStr);

        Matcher freeMatcher = freePattern.matcher(Splat.fromFile(fileName));
        Matcher itmMatcher = itmPattern.matcher(Splat.fromFile(fileName));

        double freePl = freeMatcher.find() ? Double.parseDouble(freeMatcher.group(1)) : 0;
        double itmPl = itmMatcher.find() ? Double.parseDouble(itmMatcher.group(1)) : 0;

        return itmPl != 0.0 ? itmPl : freePl; // itm value is prefered
    }

    private static CharSequence fromFile(String filename) throws IOException {
        FileInputStream input = new FileInputStream(Splat.SDF_DIR + filename);
        FileChannel channel = input.getChannel();

        // Create a read-only CharBuffer on the file
        ByteBuffer bbuf = channel.map(FileChannel.MapMode.READ_ONLY, 0, (int)channel.size());
        return StandardCharsets.ISO_8859_1.newDecoder().decode(bbuf);
    }

    private static void deleteTextFiles(String outputName, String srcName, String destName){
        new File(Splat.SDF_DIR + "/" + outputName).delete();
        new File(Splat.SDF_DIR + "/" + srcName + ".qth").delete();
        new File(Splat.SDF_DIR + "/" + destName + ".qth").delete();
        new File(Splat.SDF_DIR + "/" + srcName + "-site_report.txt").delete();
    }

    public static ConcurrentHashMap<String, ConcurrentHashMap<String, Double>> getPlDict() { return plDict; }

    public GeographicPoint getReference() { return reference; }

    public long getFetchTime() { return fetchTime; }

    public long getFetchNum() { return fetchNum; }

    public long getExecTime() { return execTime; }

    public long getExecNum() { return execNum; }

    public static void setPlDict(ConcurrentHashMap<String, ConcurrentHashMap<String, Double>> plDict) {
        Splat.plDict = plDict;
    }

    public static String getSdfDir() { return SDF_DIR; }

    public static void setSdfDir(String sdfDir) { SDF_DIR = sdfDir; }

    /**Serializing path-loss map in a file.
     * @param path path(including name) where you want to serialize the map.*/
    public static void serializePlDict(String path, String fileName) {
        if (!Files.isDirectory(Paths.get(path))) {
            try {
                Files.createDirectories(Paths.get(path));
            } catch (IOException e) {
                e.printStackTrace();
                System.out.println("Serialization was not successful! Directory creation was failed.");
                return;
            }
        }
        try(FileOutputStream fos = new FileOutputStream(String.join("/",path.split("/"))
                + "/" + fileName);
            ObjectOutputStream oos = new ObjectOutputStream(fos)) {
            oos.writeObject(plDict);
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("Serialization was not successful! Saving map failed");
        }
    }

    /**Create path-loss map from JSON file.
     * @param path JSON file path*/
    public static void readPlDictFromJson(String path){
        Type mapOfStringObjectType = new TypeToken<ConcurrentHashMap<String,
                ConcurrentHashMap<String, Double>>>() {}.getType();
        Gson gson = new Gson();
        try {
            plDict =  gson.fromJson(new FileReader(path), mapOfStringObjectType);
        } catch (FileNotFoundException e) {
            plDict = new ConcurrentHashMap<>();
            e.printStackTrace();
            System.out.println("Deserialization was not successful! File was not found.");
        }
    }

    public static void writePlDictToJson(String path){
        Type mapOfStringObjectType = new TypeToken<ConcurrentHashMap<String,
                ConcurrentHashMap<String, Double>>>() {}.getType();
        Gson gson = new Gson();
        try(FileWriter fileWriter = new FileWriter(path)) {
            gson.toJson(plDict, mapOfStringObjectType, fileWriter);
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("Serialization was not successful! Saving map failed");
        }
    }

    public static void main(String[] args) throws InterruptedException {
//        System.out.println(String.format("%04d%04d", 459, 789));
//        System.out.println(Runtime.getRuntime().availableProcessors());
//        System.exit(0);
        Splat.readPlDictFromJson("resources/splat/pl_map/pl_map.json");
//        ConcurrentHashMap<String, ConcurrentHashMap<String, Double>> map = new ConcurrentHashMap<>();
//        map.put("23", new ConcurrentHashMap<>());
//        map.get("23").put("11", 10.4);
//        map.get("23").put("14", 19.4);
//        map.put("27", new ConcurrentHashMap<>());
//        map.get("27").put("11", 105.4);
//        map.get("27").put("14", 195.4);
//        Splat.setPlDict(map);
//        Splat.writePlDictToJson("resources/splat/pl_map/pl_map_nw.json");
        ConcurrentHashMap<String, ConcurrentHashMap<String, Double>> pl_dict = Splat.getPlDict();
        long begin = System.currentTimeMillis();
        int count = 0;
        for (int srcX=0; srcX < 1001; srcX += 10)
            for (int srcY=0; srcY < 1001; srcY += 10){
                String srcKey = String.format("%04d%04d", srcX, srcY);
                for (int dstX=0; dstX < 1001; dstX += 10)
                    for (int dstY=0; dstY < 1001; dstY += 10){
                        String dstKey = String.format("%04d%04d", dstX, dstY);
                        if (pl_dict.containsKey(srcKey) && pl_dict.get(srcKey).containsKey(dstKey))
                            count++;
                        System.out.print(count + "\r");
                    }
            }
//        System.out.println(count);
        System.out.println("Number of keys: " + count + ", time: "+ (System.currentTimeMillis() - begin)/1000);
    }

    public static void deserializePlDict(String path, String fileName){
        // TODO change parameter to just one; write JavaDoc, instantiate plDIct when unsuccessful
        if (!Files.isDirectory(Paths.get(path))) {
            System.out.println("Deserialization was not successful! Directory is not existed.");
            return;
        }
        FileInputStream fis = null;
        try{
            fis = new FileInputStream(String.join("/",path.split("/"))
                    + "/" + fileName);
        }catch (FileNotFoundException e){
            e.printStackTrace();
            System.out.println("Deserialization was not successful! File was not found.");
            return;
        }
        try {
            ObjectInputStream ois = new ObjectInputStream(fis);
            plDict = (ConcurrentHashMap<String, ConcurrentHashMap<String, Double>>) ois.readObject();
            fis.close();
            ois.close();
        }catch (IOException | ClassNotFoundException e){
            e.printStackTrace();
            System.out.println("Deserialization was not successful!");
        }
    }

    /**
     * version = 1.0
     * since = 1.0
     *
     * @return Information about the propagation model.
     */
    @Override
    public String toString() {
        return null;
    }

}
