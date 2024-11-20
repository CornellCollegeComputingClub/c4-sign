package com.cornellcollegecomputingclub.java_c4sign;

import py4j.GatewayServer;
import com.cornellcollegecomputingclub.java_c4sign.JavaTaskController;

/**
 * Hello world!
 */
public class App {
    public static void main(String[] args) {
        System.out.println("Starting java gateway server...");
        GatewayServer server = new GatewayServer(new JavaTaskController());
        server.start();
        System.out.println("Java gateway server started!");
    }
}
