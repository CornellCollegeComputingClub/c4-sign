package com.cornellcollegecomputingclub.c4sign_tasks;

import java.util.Random;
import java.lang.Math;
import java.awt.geom.Path2D;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.RenderingHints;

import java.awt.image.BufferedImage;
import java.awt.image.WritableRaster;
import java.awt.Graphics2D;

import com.cornellcollegecomputingclub.java_c4sign.Constants;
import com.cornellcollegecomputingclub.java_c4sign.JavaTaskBase;

public class Lissajous extends JavaTaskBase{
    private double ratio;
    private double freqA = 1;
    private double freqB;
    private double period;
    private double phase = 0;

    public Lissajous() {
        super.setTitle("Lissajous");
        super.setArtist("Mac Coleman");
    }

    public boolean prepare() {
        Random rand = new Random();
        int a = rand.nextInt(3) + 1;
        int b = rand.nextInt(3) + 1;
        super.setTitle(a + ":" + b + " Lissajous");
        this.ratio = (double) a /(double) b; // Only rational ratios will close.
        this.freqB = freqA / this.ratio;
        this.period = Math.max(2 * Math.PI / this.freqA, 2 * Math.PI / this.freqB);
        return super.prepare();
    }

    public boolean drawFrame(BufferedImage canvas, Graphics2D graphics, WritableRaster raster, double deltaTime) {

        graphics.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        graphics.setStroke(new BasicStroke(1.5f));
        graphics.setColor(Color.WHITE);

        Path2D.Double path = new Path2D.Double();

        double firstY = 0;
        double firstX = 0;

        for (int i=0; i < 64; i++) {
            double t = ((double) i / 64.0) * 2 * this.period; // This is wrong but I am LAZY
            
            double newY = Math.sin(this.freqA * t + this.phase) * 15.0 + 16.0;
            double newX = Math.sin(this.freqB * t) * 15.0 + 16.0;
            

            if (i == 0) {
                path.moveTo(newX, newY);
                firstX = newX;
                firstY = newY;
            } else {
                path.lineTo(newX, newY);
            }
        }

        path.lineTo(firstX, firstY);
        
        graphics.draw(path);

        this.phase += deltaTime * 2.0;

        return true;
    }
}