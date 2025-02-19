package com.cornellcollegecomputingclub.c4sign_tasks;

import com.cornellcollegecomputingclub.java_c4sign.JavaTaskBase;
import com.cornellcollegecomputingclub.java_c4sign.Constants;

import java.awt.image.BufferedImage;
import java.awt.image.WritableRaster;
import java.awt.Graphics2D;

import java.lang.Math;
import java.util.Random;
import java.awt.geom.Path2D;
import java.awt.geom.Line2D;
import java.awt.geom.AffineTransform;
import java.awt.Color;
import java.awt.BasicStroke;
import java.awt.RenderingHints;

public class ArtificialHorizon extends JavaTaskBase {

    double fov = 65;
    double separationDistance;

    double pitchAngle; //pitch, limited to [-50, +50]
    double bankAngle; //roll, limited to [-45, 45]
    double yawAngle; //heading, limited to [0,360)

    double targetHeading;
    double targetAltitude;

    double kP_Altitude = 0.05;
    double kP_Heading = 1.5;

    double time;
    int changes;
    double speed = 843.905; //feet per second;
    double altitude;

    Random random;

    Path2D.Double attitudeIndicator;
    Path2D.Double slipIndicator;
    Path2D.Double slipTriangle;
    Path2D.Double pitchIndicator;
    Path2D.Double headingIndicator;
    Path2D.Double altitudeIndicator;

    public ArtificialHorizon() {
        super.setTitle("Horizon");
        super.setArtist("Mac Coleman");
    }

    public boolean prepare() {
        this.pitchAngle = 0.0;
        this.bankAngle = 0.0;
        this.yawAngle = 0.0;

        this.time = 0.0;
        this.changes = 0;
        this.altitude = 4000.0;

        this.random = new Random();

        this.attitudeIndicator = new Path2D.Double();


        this.targetAltitude = this.random.nextDouble() * 8000.0; // Pick a new altitude between 0 and 8000
        this.targetHeading = this.random.nextDouble() * 360.0 - 180.0; //I'm sure nobody will notice that it never turns all the way around :V

        this.attitudeIndicator.moveTo(16-7, 16);
        this.attitudeIndicator.lineTo(16-4, 16);
        this.attitudeIndicator.lineTo(16-2, 16+2);
        this.attitudeIndicator.lineTo(16, 16);
        this.attitudeIndicator.lineTo(16+2, 16+2);
        this.attitudeIndicator.lineTo(16+4, 16);
        this.attitudeIndicator.lineTo(16+7, 16);

        this.slipTriangle = new Path2D.Double();
        this.slipTriangle.moveTo(16, 4);
        this.slipTriangle.lineTo(17, 7);
        this.slipTriangle.lineTo(15, 7);
        this.slipTriangle.closePath();

        this.pitchIndicator = new Path2D.Double();

        this.pitchIndicator.moveTo(-11.0, 0.0);
        this.pitchIndicator.lineTo(-7.0, 0.0);

        this.pitchIndicator.moveTo(11.0, 0.0);
        this.pitchIndicator.lineTo( 7.0, 0.0);

        double pitchSeparation = (32.0 / this.fov) * 15.0;
        for (int i = 1; i < 5; i++) {
            this.pitchIndicator.moveTo(-11.0, pitchSeparation * (double) i);
            this.pitchIndicator.lineTo(-7.0, pitchSeparation * (double) i);
            this.pitchIndicator.moveTo(11.0, pitchSeparation * (double) i);
            this.pitchIndicator.lineTo( 7.0, pitchSeparation * (double) i);

            this.pitchIndicator.moveTo(-11.0, -pitchSeparation * (double) i);
            this.pitchIndicator.lineTo(-7.0, -pitchSeparation * (double) i);
            this.pitchIndicator.moveTo(11.0, -pitchSeparation * (double) i);
            this.pitchIndicator.lineTo( 7.0, -pitchSeparation * (double) i);
        }

        this.slipIndicator = new Path2D.Double();

        for (int i = 0; i<64; i++) {
            double x = 10.0 * Math.cos(Math.PI/180.0 * 180.0 * -(1.0 + (double) i) / 64.0);
            double y = 10.0 * Math.sin(Math.PI/180.0 * 180.0 * -(1.0 + (double) i) / 64.0);

            if (i == 0) {
                this.slipIndicator.moveTo(x, y);
            } else {
                this.slipIndicator.lineTo(x, y);
            }
        }

        this.slipIndicator.moveTo(0.0, -10.0);
        this.slipIndicator.lineTo(0.0, -8.0);
        this.slipIndicator.moveTo(-10.0, 0.0);
        this.slipIndicator.lineTo(-8.0, 0.0);
        this.slipIndicator.moveTo(10.0, 0.0);
        this.slipIndicator.lineTo(8.0, 0.0);

        this.headingIndicator = new Path2D.Double();

        this.headingIndicator.moveTo(0.0, 0.0);
        this.headingIndicator.lineTo(0.0, -3.0);

        double fifteenDegreeOffset = (32.0 / this.fov) * 15.0;
        this.separationDistance = fifteenDegreeOffset;
        
        for (int i = 1; i < 5; i++) {
            double height = i % 2 == 1 ? -2.0 : -3.0;
            this.headingIndicator.moveTo((double) i * fifteenDegreeOffset, 0.0);
            this.headingIndicator.lineTo((double) i * fifteenDegreeOffset, height);
            this.headingIndicator.moveTo((double) i * -fifteenDegreeOffset, 0.0);
            this.headingIndicator.lineTo((double) i * -fifteenDegreeOffset, height);
        }

        this.altitudeIndicator = (Path2D.Double) this.headingIndicator.clone();
        AffineTransform a = new AffineTransform();
        a.setToRotation(-Math.PI/2);
        this.altitudeIndicator.transform(a);
        return super.prepare();
    }

    public boolean drawFrame(BufferedImage canvas, Graphics2D graphics, WritableRaster raster, double deltaTime) {

        this.time += deltaTime;
        int t = (int) (this.time / 10.0);

        if (t != this.changes) {
            //choose a new heading and altitude every ten seconds
            this.changes = t;

            if (this.random.nextInt(2) == 1) {
                this.targetAltitude = this.random.nextDouble() * 8000.0; // Pick a new altitude between 0 and 8000
            } else {
                this.targetHeading = this.random.nextDouble() * 360.0 - 180.0;
            }
        }

        double newPitchCorrection = Math.min(Math.max((this.targetAltitude - this.altitude) * this.kP_Altitude, -25.0), 25.0) - this.pitchAngle;
        this.pitchAngle += Math.min(Math.max(newPitchCorrection, -5.0 * deltaTime), 5.0 * deltaTime);
        double newBankCorrection = Math.min(Math.max((this.targetHeading - this.yawAngle) * this.kP_Heading, -35.0), 35.0) - this.bankAngle;
        this.bankAngle += Math.min(Math.max(newBankCorrection, -15.0 * deltaTime), 15.0 * deltaTime);
        this.yawAngle += Math.sin(Math.PI / 180.0 * this.bankAngle) * deltaTime * 25.0; //degrees per second at full roll...;
        this.yawAngle %= 360;
        this.altitude += Math.sin(Math.PI/180.0 * this.pitchAngle) * deltaTime * this.speed;

        graphics.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        graphics.setClip(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT);

        graphics.setColor(new Color(0x22, 0xa1, 0xfd)); //Sky color
        graphics.fillRect(0, 0, 32, 32);

        graphics.setColor(new Color(0x8e, 0x62, 0x37)); //Ground color

        Path2D.Double ground = new Path2D.Double();

        double bankOffset = 16.0 * Math.tan(Math.PI / 180 * this.bankAngle);
        double pitchOffset = (32 / this.fov) * this.pitchAngle / Math.cos(Math.PI / 180 * this.bankAngle);
        ground.moveTo(0, 16 + pitchOffset - bankOffset);
        ground.lineTo(32, 16 + pitchOffset + bankOffset);
        ground.lineTo(32, 32);
        ground.lineTo(0, 32);
        ground.closePath();

        graphics.fill(ground);

        graphics.setColor(Color.WHITE);
        graphics.setStroke(new BasicStroke(1.0f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_ROUND));

        graphics.draw(this.attitudeIndicator);

        AffineTransform a = new AffineTransform();

        double headingOffset = (32 / this.fov) * (this.yawAngle % 30.0);
        a.setToTranslation(16.0 + headingOffset, 32.0);
        Path2D.Double headingIndicator = (Path2D.Double) this.headingIndicator.clone();
        headingIndicator.transform(a);
        graphics.draw(headingIndicator);

        Path2D.Double slipIndicator = (Path2D.Double) this.slipIndicator.clone();
        a.setToRotation(this.bankAngle * Math.PI/180.0);
        slipIndicator.transform(a);
        a.setToTranslation(16.0, 16.0);
        slipIndicator.transform(a);
        graphics.draw(slipIndicator);
        //graphics.draw(this.slipTriangle);

        graphics.setClip(3, 0, 26, 29);

        double pitchIndicatorOffset = (32.0 / this.fov) * this.pitchAngle;

        Path2D.Double transformedIndicator = (Path2D.Double) this.pitchIndicator.clone();
        a.setToTranslation(0, pitchIndicatorOffset);
        transformedIndicator.transform(a);
        a.setToRotation(this.bankAngle * Math.PI / 180.0);
        //t.translate(16.0, 16.0);
        transformedIndicator.transform(a);
        a.setToTranslation(16.0, 16.0);
        transformedIndicator.transform(a);
        graphics.draw(transformedIndicator);

        graphics.setClip(29, 0, 3, 26);

        double altitudeOffset = (this.separationDistance / 100.0) * (this.altitude % 200.0); //each tick is 250 feet
        a.setToTranslation(32.0, 16.0 + altitudeOffset);
        Path2D.Double altitudeIndicator = (Path2D.Double) this.altitudeIndicator.clone();
        altitudeIndicator.transform(a);
        graphics.draw(altitudeIndicator);

        return false;
    }
}
