package edu.stonybrook.cs.wingslab.commons;

import junit.framework.TestCase;

public class SplatSiteTest extends TestCase {

    public void testTestGetName() {
        SplatSite sp1 = new SplatSite(SiteType.TX, new GeographicPoint(1.0, -2.0), 15.0);
        System.out.println(sp1.getName());
    }

    public void testTestToString() {
        SplatSite sp1 = new SplatSite(SiteType.TX, new GeographicPoint(1.0, -2.0), 15.0);
        System.out.println(sp1);
    }

    public void testCreateQTHFile() {
        SplatSite sp1 = new SplatSite(SiteType.TX, new GeographicPoint(1.0, -2.0), 15.0);
        sp1.CreateQTHFile("resources/splat/sdf");
    }
}