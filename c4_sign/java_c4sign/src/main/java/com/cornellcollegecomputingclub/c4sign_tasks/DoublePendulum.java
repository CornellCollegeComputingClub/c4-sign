package com.cornellcollegecomputingclub.c4sign_tasks;

import com.cornellcollegecomputingclub.java_c4sign.JavaTaskBase;
import com.cornellcollegecomputingclub.java_c4sign.VerletParticle;

import java.util.Random;
import java.awt.image.BufferedImage;
import java.awt.image.WritableRaster;
import java.awt.Graphics2D;
import java.awt.BasicStroke;
import java.awt.RenderingHints;
import java.awt.Color;
import java.awt.geom.Line2D;
import java.awt.geom.Path2D;

import org.apache.commons.math3.geometry.euclidean.twod.Vector2D;

public class DoublePendulum extends JavaTaskBase {
    private Vector2D anchor;
    private VerletParticle point1;
    private VerletParticle point2;
    private double length;
    private Vector2D gravity;

    private Vector2D[] pastPositions;
    private int index;

    private float hue;

    public DoublePendulum() {
        this.setArtist("Mac Coleman");
        this.setTitle("Double Pendulum");
    }
    
    public boolean prepare() {

        this.length = 8.0;

        Random r = new Random();
        double theta = (r.nextDouble()-0.5) * Math.PI / 180.0;
        double phi = (r.nextDouble()-0.5) * Math.PI / 180.0;

        double x1 = 16.0 + Math.sin(theta) * this.length;
        double y1 = 16.0 - Math.cos(theta) * this.length;

        double x2 = x1 + Math.sin(phi) * this.length;
        double y2 = y1 - Math.cos(phi) * this.length;

        this.anchor = new Vector2D(16.0, 16.0);
        this.point1 = new VerletParticle(x1, y1);
        this.point2 = new VerletParticle(x2, y2);



        //Expressing g in pixels/sec^2
        // 32 pixels over 13 inches
        // 0.0254 meters per inch
        // 9.81 m/s^2
        // multiplied by a scaling factor
        double g = (32.0 / 13.0) * (1 / 0.0254) * 9.81 * 0.125;

        this.gravity = new Vector2D(0.0, g);

        this.pastPositions = new Vector2D[64];
        this.index = 0;

        this.hue = 0.0f;

        return super.prepare();
    }

    public boolean drawFrame(BufferedImage canvas, Graphics2D graphics, WritableRaster raster, double timeDelta) {

        int steps = 128;
        for (int i = 0; i < steps; i++) {
            this.point1.accelerate(this.gravity);
            this.point2.accelerate(this.gravity);

            this.point2.applyLinkToParticleConstraint(this.point1, this.length);
            this.point1.applyLinkToAnchorConstraint(this.anchor, this.length);

            this.point1.updatePosition(timeDelta/(double) steps);
            this.point2.updatePosition(timeDelta/(double) steps);
        }

        this.pastPositions[this.index] = this.point2.getPosition();


        graphics.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        graphics.setStroke(new BasicStroke(1.0f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_ROUND));

        int c = 0;
        for (int i = this.index; i > this.index-this.pastPositions.length+1; i--) {
            int i_a = ((i % this.pastPositions.length) + this.pastPositions.length) % this.pastPositions.length;
            int i_b = (((i - 1) % this.pastPositions.length) + this.pastPositions.length) % this.pastPositions.length;
            Vector2D a = this.pastPositions[i_a];
            Vector2D b = this.pastPositions[i_b];

            if (a == null || b == null) {
                break;
            }

            float r = 1.0f - (float) c / (float) this.pastPositions.length;
            Color temp = Color.getHSBColor(this.hue, 1.0f, 1.0f);
            graphics.setColor(new Color(temp.getRed(), temp.getGreen(), temp.getBlue(), (int) (255 * r)));
            graphics.draw(new Line2D.Double(a.getX(), a.getY(), b.getX(), b.getY()));
            c++;
        }

        Path2D.Double line = new Path2D.Double();
        line.moveTo(this.anchor.getX(), this.anchor.getY());
        line.lineTo(this.point1.getPosition().getX(), this.point1.getPosition().getY());
        line.lineTo(this.point2.getPosition().getX(), this.point2.getPosition().getY());

        graphics.setColor(Color.WHITE);
        graphics.draw(line);

        this.index++;
        this.index %= this.pastPositions.length;

        this.hue += timeDelta * 1.0f / 60.0f;

        return false;
    };

    public void teardown(boolean forced) {
        super.teardown(forced);

        this.anchor = null;
        this.point1 = null;
        this.point2 = null;
        this.gravity = null;
        this.pastPositions = null;
    }
}
