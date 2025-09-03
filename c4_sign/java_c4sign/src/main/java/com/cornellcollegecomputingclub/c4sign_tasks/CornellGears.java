package com.cornellcollegecomputingclub.c4sign_tasks;

import com.cornellcollegecomputingclub.java_c4sign.JavaTaskBase;

import java.awt.image.BufferedImage;
import java.awt.Graphics2D;
import java.awt.image.WritableRaster;

import java.awt.Color;
import java.awt.RenderingHints;
import java.awt.geom.Path2D;
import java.awt.geom.AffineTransform;

import com.cornellcollegecomputingclub.java_c4sign.VerletParticle;
import org.apache.commons.math3.geometry.euclidean.twod.Vector2D;


public class CornellGears extends JavaTaskBase {

    double outerRadius = 14;
    double innerRadius = 10;
    int teeth = 8;
    double toothTopPortion = 0.35;
    double toothBottomPortion = 0.35;
    double toothSlopePortion = (1.0 - toothTopPortion - toothBottomPortion) / 2.0;
    double angle = 0.0;
    double angularVelocity = 3.0; //Rads/sec

    double teeth2 = 6;
    double outerRadius2 = teeth2/teeth * outerRadius;
    double innerRadius2 = outerRadius2 - (outerRadius - innerRadius);

    double length = 50.0;

    Path2D.Double gear1;
    Path2D.Double gear2;
    Path2D.Double cornellC;
    Path2D.Double rod;

    VerletParticle slider;

    public CornellGears () {
        super.setTitle("Cornell Gears");
        super.setArtist("Mac Coleman");
    }

    public boolean prepare() {
        this.angle = 0.0;

        double sectorSubtendedAngle = 360.0 / this.teeth;

        this.gear1 = new Path2D.Double();

        this.gear1.moveTo(Math.cos(0) * this.innerRadius, -Math.sin(0) * this.innerRadius);
        for (int i = 0; i < this.teeth; i++) {
            double angle = (sectorSubtendedAngle * i) * Math.PI/180.0;
            angle += (toothBottomPortion/2.0) * sectorSubtendedAngle * Math.PI/180.0;
            this.gear1.lineTo(Math.cos(angle) * this.innerRadius, -Math.sin(angle) * this.innerRadius);
            angle += toothSlopePortion * sectorSubtendedAngle * Math.PI/180.0;
            this.gear1.lineTo(Math.cos(angle) * this.outerRadius, -Math.sin(angle) * this.outerRadius);
            angle += toothTopPortion * sectorSubtendedAngle * Math.PI/180.0;
            this.gear1.lineTo(Math.cos(angle) * this.outerRadius, -Math.sin(angle) * this.outerRadius);
            angle += toothSlopePortion * sectorSubtendedAngle * Math.PI/180.0;
            this.gear1.lineTo(Math.cos(angle) * this.innerRadius, -Math.sin(angle) * this.innerRadius);
            angle += (toothBottomPortion/2.0) * sectorSubtendedAngle * Math.PI/180.0;
            this.gear1.lineTo(Math.cos(angle) * this.innerRadius, -Math.sin(angle) * this.innerRadius);
        }

        sectorSubtendedAngle = 370.0 / this.teeth2;

        this.gear2 = new Path2D.Double();

        this.gear2.moveTo(Math.cos(0) * this.innerRadius2, -Math.sin(0) * this.innerRadius2);
        for (int i = 0; i < this.teeth2; i++) {
            double angle = (sectorSubtendedAngle * i) * Math.PI/180.0;
            angle += (toothBottomPortion/2.0) * sectorSubtendedAngle * Math.PI/180.0;
            this.gear2.lineTo(Math.cos(angle) * this.innerRadius2, -Math.sin(angle) * this.innerRadius2);
            angle += toothSlopePortion * sectorSubtendedAngle * Math.PI/180.0;
            this.gear2.lineTo(Math.cos(angle) * this.outerRadius2, -Math.sin(angle) * this.outerRadius2);
            angle += toothTopPortion * sectorSubtendedAngle * Math.PI/180.0;
            this.gear2.lineTo(Math.cos(angle) * this.outerRadius2, -Math.sin(angle) * this.outerRadius2);
            angle += toothSlopePortion * sectorSubtendedAngle * Math.PI/180.0;
            this.gear2.lineTo(Math.cos(angle) * this.innerRadius2, -Math.sin(angle) * this.innerRadius2);
            angle += (toothBottomPortion/2.0) * sectorSubtendedAngle * Math.PI/180.0;
            this.gear2.lineTo(Math.cos(angle) * this.innerRadius2, -Math.sin(angle) * this.innerRadius2);
        }

        this.cornellC = new Path2D.Double();

        this.cornellC.moveTo(3, -3);
        this.cornellC.lineTo(3, -4);
        this.cornellC.lineTo(2, -5.5);
        this.cornellC.lineTo(-2,-5.5);
        this.cornellC.lineTo(-3,-4);
        this.cornellC.lineTo(-3, 4);
        this.cornellC.lineTo(-2, 5.5);
        this.cornellC.lineTo(2, 5.5);
        this.cornellC.lineTo(3, 4);
        this.cornellC.lineTo(3, 3);

        this.rod = new Path2D.Double();
        this.rod.moveTo(0, 1.5);
        this.rod.lineTo(-.5, 1);
        this.rod.lineTo(-.5, -1);
        this.rod.lineTo(0, -1.5);
        this.rod.lineTo(this.length, -1.5);
        this.rod.lineTo(this.length + 0.5, -1);
        this.rod.lineTo(this.length + 0.5, 1);
        this.rod.lineTo(this.length, 1.5 );
        this.rod.lineTo(0, 1.5);

        this.slider = new VerletParticle(16 + this.length, 16);

        return super.prepare();
    }

    public boolean drawFrame(BufferedImage canvas, Graphics2D graphics, WritableRaster raster, double deltaTime) {
        graphics.setColor(Color.WHITE);
        graphics.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        Path2D.Double gear1Transformed = (Path2D.Double) this.gear1.clone();
        AffineTransform a = new AffineTransform();

        this.angle += this.angularVelocity * deltaTime;
        a.setToRotation(this.angle);
        gear1Transformed.transform(a);

        a.setToTranslation(16.0, 16.0);
        gear1Transformed.transform(a);

        Path2D.Double gear2Transformed = (Path2D.Double) this.gear2.clone();
        a.setToRotation(-this.teeth/this.teeth2 * this.angle + 15.0 * Math.PI/180.0);
        gear2Transformed.transform(a);

        a.setToTranslation(16.0 + Math.cos(135 * Math.PI/180.0) * (this.innerRadius + this.outerRadius2), 16.0 - Math.sin(135 * Math.PI/180.0) * (this.innerRadius + this.outerRadius2));
        gear2Transformed.transform(a);

        Path2D.Double gear3Transformed = (Path2D.Double) this.gear2.clone();
        a.setToRotation(-this.teeth/this.teeth2 * this.angle + 105.0 * Math.PI/180.0);
        gear3Transformed.transform(a);

        a.setToTranslation(16.0 + Math.cos(225 * Math.PI/180.0) * (this.innerRadius + this.outerRadius2), 16.0 - Math.sin(225 * Math.PI/180.0) * (this.innerRadius + this.outerRadius2));
        gear3Transformed.transform(a);

        Path2D.Double cornellCTransformed = (Path2D.Double) this.cornellC.clone();
        a.setToRotation(this.angle);
        cornellCTransformed.transform(a);
        a.setToTranslation(16.0, 16.0);
        cornellCTransformed.transform(a);

        Vector2D anchor = new Vector2D(16.0 + 8.0 * Math.cos(-this.angle), 16.0 + 8.0 * -Math.sin(-this.angle));
        //I guess AffineTransform's rotation is clockwise????

        int steps = 128;
        for (int i = 0; i < steps; i++) {
            this.slider.applyLinearMotionConstraint(new Vector2D(0.0, 16.0), new Vector2D(32.0, 16.0));
            this.slider.applyLinkToAnchorConstraint(anchor, this.length);

            this.slider.updatePosition(deltaTime/(double) steps);
        }

        Path2D.Double rodTransformed = (Path2D.Double) this.rod.clone();
        Vector2D rodDirection = this.slider.getPosition().subtract(anchor);

        a.setToRotation(Math.atan2(rodDirection.getY(), rodDirection.getX()));
        rodTransformed.transform(a);

        a.setToTranslation(anchor.getX(), anchor.getY());
        rodTransformed.transform(a);

        graphics.draw(gear1Transformed);
        graphics.draw(gear2Transformed);
        graphics.draw(gear3Transformed);

        graphics.setColor(new Color(191, 90, 242));
        graphics.draw(cornellCTransformed);

        graphics.setColor(Color.BLACK);
        graphics.fill(rodTransformed);
        graphics.setColor(Color.WHITE);
        graphics.draw(rodTransformed);

        return true;
    }

    public void teardown(boolean forced) {

        this.gear1 = null;
        this.gear2 = null;
        this.cornellC = null;
        this.rod = null;
        this.slider = null;

        super.teardown(forced);
    }
}
