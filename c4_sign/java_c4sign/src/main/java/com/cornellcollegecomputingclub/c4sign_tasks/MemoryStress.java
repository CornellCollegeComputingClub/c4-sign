package com.cornellcollegecomputingclub.c4sign_tasks;

import java.lang.Math;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import com.cornellcollegecomputingclub.java_c4sign.Constants;
import com.cornellcollegecomputingclub.java_c4sign.JavaTaskBase;

public class MemoryStress extends JavaTaskBase {
    public byte[] iLoveMemory;
    private Random random = new Random();

    public MemoryStress() {
        super.setTitle("JVMMemory Stress");
        super.setArtist("Luna");
    }

    public boolean prepare() {
        return super.prepare();
    }

    public boolean drawFrame(byte[][][] canvas, double deltaTime) {
        iLoveMemory = new byte[1024 * 1024]; // 1MB
        // do something
        for (int i = 0; i < iLoveMemory.length; i++) {
            iLoveMemory[i] = (byte) random.nextInt(256);
        }

        // draw a pixel for every 10MB allocated
        int memorySize = (int) (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory());
        try {
            for (int i = 0; i < memorySize; i += 1 * 1024 * 1024) {
                int j = i / 1 / 1024 / 1024;
                int x = j % Constants.SCREEN_WIDTH;
                int y = j / Constants.SCREEN_WIDTH;
                canvas[x][y] = new byte[] { (byte) 0xFF, (byte) 0xFF, (byte) 0xFF };
            }
        } catch (ArrayIndexOutOfBoundsException e) {
            // ignore
        }
        return false;
    }

    public void teardown(boolean forced) {
        this.iLoveMemory = null;

        System.gc(); // suggest garbage collection
    }
}
