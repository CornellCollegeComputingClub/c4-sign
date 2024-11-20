package com.cornellcollegecomputingclub.c4sign_tasks;

import java.util.Random;

import com.cornellcollegecomputingclub.java_c4sign.Constants;
import com.cornellcollegecomputingclub.java_c4sign.JavaTaskBase;

public class RainbowWaveJava extends JavaTaskBase {
    byte[][] epic_colors;
    Random rand;

    public RainbowWaveJava() {
        super.setTitle("Rainbow Wave");
        super.setArtist("Mac Coleman");

        this.rand = new Random();
    }

    public boolean drawFrame(byte[][][] canvas, double deltaTime) {
        for (int i = 0; i < Constants.SCREEN_WIDTH; i++) {
            for (int j = 0; j < Constants.SCREEN_HEIGHT; j++) {
                rand.nextBytes(canvas[i][j]);
            }
        }
        return true;
    }
}
