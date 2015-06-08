package edu.stsci.mast.osdd.app;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

import javax.ws.rs.ApplicationPath;
import javax.ws.rs.core.Application;

import edu.stsci.mast.osdd.rest.DeliverData;

@ApplicationPath("/rest")
public class Osdd extends Application {
    public Set<Class<?>> getClasses() {
        return new HashSet<Class<?>>(Arrays.asList(DeliverData.class));
    }
}