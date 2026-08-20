package com.cornellcollegecomputingclub.java_c4sign;

import org.apache.commons.math3.geometry.euclidean.twod.Vector2D;

public class VerletParticle {
    private Vector2D lastPosition;
    private Vector2D currentPosition;
    private Vector2D acceleration;

    public VerletParticle() {
        this.currentPosition = new Vector2D(0.0, 0.0);
        this.lastPosition = new Vector2D(0.0, 0.0);
        this.acceleration = new Vector2D(0.0, 0.0);
    }

    public VerletParticle(double x, double y) {
        this.currentPosition = new Vector2D(x, y);
        this.lastPosition = this.currentPosition;
        this.acceleration = new Vector2D(0.0, 0.0);
    }

    public VerletParticle(double x, double y, double velocityX, double velocityY) {
        this.currentPosition = new Vector2D(x, y);
        this.lastPosition = this.currentPosition.add(new Vector2D(- velocityX, -velocityY));
        this.acceleration = new Vector2D(0.0, 0.0);
    }

    public void accelerate(Vector2D acceleration) {
        this.acceleration = this.acceleration.add(acceleration);
    }

    public void accelerate(double x, double y) {
        this.acceleration = this.acceleration.add(new Vector2D(x, y));
    }

    public void updatePosition(double deltaTime) {
        Vector2D velocity = this.currentPosition.subtract(this.lastPosition);
        this.lastPosition = this.currentPosition;
        this.currentPosition = this.currentPosition.add(velocity).add(this.acceleration.scalarMultiply(deltaTime * deltaTime));
        this.acceleration = new Vector2D(0.0, 0.0);
    }

    /**
     * If the particle is farther away from the anchor point than length, it moves the particle back within length of the anchor point.
     * @param anchorPoint The point the particle is constrained to.
     * @param length The distance the particle is constrained within.
     */
    public void applyLengthConstraint(Vector2D anchorPoint, double length) {
        if (this.currentPosition.distance(anchorPoint) > length) {
            this.currentPosition = anchorPoint.add(this.currentPosition.subtract(anchorPoint).normalize().scalarMultiply(length));
        }
    }

    /**
     * Constraints the particle to always be length away from anchorPoint.
     * @param anchorPoint The point the particle is constrained to.
     * @param length The distance away from the anchor point that the particle is constrained to.
     */
    public void applyLinkToAnchorConstraint(Vector2D anchorPoint, double length) {
        this.currentPosition = anchorPoint.add(this.currentPosition.subtract(anchorPoint).normalize().scalarMultiply(length));
    }

    public void applyLinkToParticleConstraint(VerletParticle other, double length) {
        //Find difference to desired length
        //Move both particles half of the desired difference towards/away from each other.
        double overshoot = this.currentPosition.distance(other.getPosition()) - length;
        Vector2D toOther = other.getPosition().subtract(this.currentPosition).normalize().scalarMultiply(overshoot/2.0);
        this.currentPosition = this.currentPosition.add(toOther);
        other.setPosition(other.getPosition().subtract(toOther));
    }

    public void applyLinearMotionConstraint(Vector2D linePoint1, Vector2D linePoint2) {

        double x0 = this.currentPosition.getX();
        double y0 = this.currentPosition.getY();
        double x1 = linePoint1.getX();
        double x2 = linePoint2.getX();
        double y1 = linePoint1.getY();
        double y2 = linePoint2.getY();

        double distanceFromLine = Math.abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1) / Math.sqrt(Math.pow(y2 -y1, 2) + Math.pow(x2 - x1, 2));
        Vector2D lineNormal = new Vector2D(-(y2 -y1), x2 - x1).normalize();

        Vector2D relativeToPoint = this.currentPosition.subtract(linePoint1);
        if (Vector2D.angle(lineNormal, relativeToPoint) < Math.PI/2) {
            distanceFromLine *= -1;
        }

        Vector2D correction = lineNormal.scalarMultiply(distanceFromLine);
        this.currentPosition = this.currentPosition.add(correction);
    }

    public Vector2D getPosition() {
        return this.currentPosition;
    }

    public void setPosition(Vector2D newPosition) {
        this.currentPosition = newPosition;
    }
}