package com.cornellcollegecomputingclub.java_c4sign;

import java.awt.image.WritableRaster;
import java.awt.image.DataBufferByte;

public class TaskResult {
    private WritableRaster raster;
    private boolean finished;

    public TaskResult(WritableRaster w, boolean f) {
        this.raster = w;
        this.finished = f;
    }

    public byte[] getCanvas() {
        return ((DataBufferByte) this.raster.getDataBuffer()).getData();
    }

    public boolean isFinished() {
        return this.finished;
    }
}