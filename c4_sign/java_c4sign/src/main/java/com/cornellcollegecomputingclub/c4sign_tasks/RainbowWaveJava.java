package com.cornellcollegecomputingclub.c4sign_tasks;

import java.lang.Math;

import java.awt.image.BufferedImage;
import java.awt.image.WritableRaster;
import java.awt.Graphics2D;

import com.cornellcollegecomputingclub.java_c4sign.Constants;
import com.cornellcollegecomputingclub.java_c4sign.JavaTaskBase;

public class RainbowWaveJava extends JavaTaskBase {
    private int[][] epic_colors;
    private int frame;

    public RainbowWaveJava() {
        super.setTitle("RainbowWaveJava");
        super.setArtist("Mac Coleman");
    }

    public boolean prepare() {
        this.frame = 0;
        this.epic_colors = new int[][] {
            {0xFF, 0x00, 0x00},
            {0XFF, 0X60, 0X00},
            {0XFF, 0XBF, 0X00},
            {0XB5, 0XFF, 0X00},
            {0X80, 0XFF, 0X00},
            {0X20, 0XFF, 0X00},
            {0X00, 0XFF, 0X40},
            {0X00, 0XFF, 0XFF},
            {0X00, 0X9F, 0XFF},
            {0X00, 0X40, 0XFF},
            {0X20, 0X00, 0XFF},
            {0X7F, 0X00, 0XFF},
            {0XDF, 0X00, 0XFF},
            {0XFF, 0X00, 0XBF},
            {0XFF, 0X00, 0X60},
        };

        return super.prepare();
    }

    public boolean drawFrame(BufferedImage canvas, Graphics2D graphics, WritableRaster raster, double deltaTime) {
        for (int i = 0; i < Constants.SCREEN_WIDTH; i++) {
            for (int j = 0; j < Constants.SCREEN_HEIGHT; j++) {
                int signedIndex = (int) (Math.floor(Math.sqrt(Math.pow(15.5-i, 2) + Math.pow(15.5-j, 2)) - this.frame)) % this.epic_colors.length;
                int unsignedIndex = (this.epic_colors.length + signedIndex) % this.epic_colors.length;
                raster.setPixel(i, j, this.epic_colors[unsignedIndex]);
            }
        }
        this.frame += 1;
        return true;
    }

    public void teardown(boolean forced) {
        this.epic_colors = null;
        super.teardown(forced);
    }
}
