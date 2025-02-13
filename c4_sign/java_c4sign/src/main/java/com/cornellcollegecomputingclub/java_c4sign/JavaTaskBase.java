package com.cornellcollegecomputingclub.java_c4sign;

import com.cornellcollegecomputingclub.java_c4sign.Constants;
import com.cornellcollegecomputingclub.java_c4sign.TaskResult;

import java.awt.image.BufferedImage;
import java.awt.image.WritableRaster;
import java.awt.Graphics2D;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;

import org.apache.commons.lang3.StringUtils;

public abstract class JavaTaskBase {
    private String title;
    private String artist;
    private BufferedImage canvas;
    private WritableRaster raster;
    private Graphics2D graphics;
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
        this.canvas = new BufferedImage(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, BufferedImage.TYPE_3BYTE_BGR);
        this.raster = this.canvas.getRaster();
        this.graphics = this.canvas.createGraphics();
        return true;
    }


    public void teardown(boolean forced) {
        /**
        * Teardown: This method is called when the task stops running.
        * If the task was stopped forcefully, the forced parameter will be true.
        * If your task requires special cleanup, override this method!
        */
        this.canvas = null;
        this.raster = null;
        this.graphics.dispose();
    }

    public abstract boolean drawFrame(BufferedImage canvas, Graphics2D graphics, WritableRaster raster, double timeDelta);

    public TaskResult draw(double timeDelta) {
        this.graphics.clearRect(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT);
        boolean finished = this.drawFrame(this.canvas, this.graphics, this.raster, timeDelta);

        //We're all synchronous here, right? 
        return new TaskResult(this.raster, finished);
    }

    public BufferedImage retrieveCanvas() {
        return this.canvas;
    }

    public String getLcdText() {
        String line1 = StringUtils.center(this.title, Constants.LCD_WIDTH).substring(0, Constants.LCD_WIDTH);
        String line2 = "By:";
        line2 = line2.concat(StringUtils.center(this.artist, Constants.LCD_WIDTH - 3).substring(0, Constants.LCD_WIDTH - 3));
        return line1.concat(line2);
    }

    public String toString() {
        return this.title.concat(" by ").concat(this.artist);
    }
}
