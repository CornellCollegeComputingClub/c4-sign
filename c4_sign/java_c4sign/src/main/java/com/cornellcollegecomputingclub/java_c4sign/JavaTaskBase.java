package com.cornellcollegecomputingclub.java_c4sign;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;

import org.apache.commons.lang3.StringUtils;

public abstract class JavaTaskBase {
    private String title;
    private String artist;
    private byte[][][] canvas;

    public JavaTaskBase() {
        this.title = "Unknown";
        this.artist = "Unknown";
        this.canvas = new byte[32][32][3];
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

    public abstract boolean drawFrame(byte[][][] canvas, double timeDelta);

    public boolean draw(double timeDelta) {
        this.canvas = new byte[32][32][3];
        boolean finished = this.drawFrame(this.canvas, timeDelta);
        return finished;
    }

    public byte[] retrieveCanvas() {
        ByteBuffer intBuffer = ByteBuffer.allocate(3*32*32);
        intBuffer.order(ByteOrder.LITTLE_ENDIAN);

        for (int i = 0; i < 32; i++) {
            for (int j = 0; j < 32; j++) {
                intBuffer.put(this.canvas[i][j]);
            }
        }

        return intBuffer.array();
    }

    public String getLcdText() {
        String line1 = StringUtils.center(this.title, 16).substring(0, 16);
        String line2 = "By: ";
        line2 = line2.concat(StringUtils.center(this.artist, 16)).substring(0, 16);
        return line1.concat(line2);
    }
}
