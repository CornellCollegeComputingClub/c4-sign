package com.cornellcollegecomputingclub.java_c4sign;

import com.cornellcollegecomputingclub.java_c4sign.Constants;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;

import org.apache.commons.lang3.StringUtils;

public abstract class JavaTaskBase {
    private String title;
    private String artist;
    private byte[][][] canvas;
    public static boolean ignore = false;

    public JavaTaskBase() {
        this.title = "Unknown";
        this.artist = "Unknown";
    }

    public void setTitle(String newTitle) {
        this.title = newTitle;
    }

    public String getTitle() {
        return this.title;
    }

    public void setArtist(String newArtist) {
        this.artist = newArtist;
    }

    public String getArtist() {
        return this.artist;
    }

    public boolean prepare() {
        /**
         * This method is called when the task is first run.
         * If this method returns false, the task will be skipped.
         * If this method returns true, the task will be run.
         */
        this.canvas = new byte[Constants.SCREEN_WIDTH][Constants.SCREEN_HEIGHT][Constants.SCREEN_COLORS];
        return true;
    }


    public void teardown(boolean forced) {
        /**
        * Teardown: This method is called when the task stops running.
        * If the task was stopped forcefully, the forced parameter will be true.
        * If your task requires special cleanup, override this method!
        */
        this.canvas = null;
    }

    public abstract boolean drawFrame(byte[][][] canvas, double timeDelta);

    public boolean draw(double timeDelta) {
        this.canvas = new byte[Constants.SCREEN_WIDTH][Constants.SCREEN_HEIGHT][Constants.SCREEN_COLORS];
        boolean finished = this.drawFrame(this.canvas, timeDelta);
        return finished;
    }

    public byte[] retrieveCanvas() {
        ByteBuffer intBuffer = ByteBuffer.allocate(Constants.SCREEN_COLORS*Constants.SCREEN_WIDTH*Constants.SCREEN_HEIGHT);
        intBuffer.order(ByteOrder.LITTLE_ENDIAN);

        for (int i = 0; i < Constants.SCREEN_WIDTH; i++) {
            for (int j = 0; j < Constants.SCREEN_HEIGHT; j++) {
                intBuffer.put(this.canvas[i][j]);
            }
        }

        return intBuffer.array();
    }

    public String getLcdText() {
        String line1 = StringUtils.center(this.title, Constants.LCD_WIDTH).substring(0, Constants.LCD_WIDTH);
        String line2 = "By: ";
        line2 = line2.concat(StringUtils.center(this.artist, Constants.LCD_WIDTH)).substring(0, Constants.LCD_WIDTH);
        return line1.concat(line2);
    }

    public String toString() {
        return this.title.concat(" by ").concat(this.artist);
    }
}