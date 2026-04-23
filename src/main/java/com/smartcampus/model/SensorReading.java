package com.smartcampus.model;

public class SensorReading {
    private String id;           // Distinct reading ID
    private long timestamp;      // Timestamp in milliseconds
    private double value;        // Recorded metric value

    public SensorReading() {}

    public SensorReading(String id, long timestamp, double value) {
        this.id = id;
        this.timestamp = timestamp;
        this.value = value;
    }

    // Accessor methods (get/set)
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public long getTimestamp() { return timestamp; }
    public void setTimestamp(long timestamp) { this.timestamp = timestamp; }

    public double getValue() { return value; }
    public void setValue(double value) { this.value = value; }
}