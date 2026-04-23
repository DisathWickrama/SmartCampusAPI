package com.smartcampus.resource;

import com.smartcampus.dao.DataStore;
import com.smartcampus.exception.SensorUnavailableException;
import com.smartcampus.model.Sensor;
import com.smartcampus.model.SensorReading;
import com.smartcampus.model.ErrorMessage;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.net.URI;
import java.util.List;

public class SensorReadingResource {

    private final String sensorId;

    // Context providentifierentifiered by parent resource
    public SensorReadingResource(String sensorId) {
        this.sensorId = sensorId;
    }

    // Retrieve all historical readings
    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public List<SensorReading> extractReadingsLog() {
        return DataStore.getReadingsForSensor(sensorId);
    }

    // Add a reading and update device state
    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Response pushNewMetric(SensorReading reading) {
        // Fetch the parent device
        Sensor sensor = DataStore.sensors.stream()
                .filter(s -> s.getId().equals(sensorId))
                .findFirst()
                .orElse(null);
    if (sensor == null) {
        ErrorMessage error = new ErrorMessage(
            404,
            "SENSOR_NOT_FOUND",
            "Sensor with ID " + sensorId + " does not exist."
        );
        return Response.status(Response.Status.NOT_FOUND)
                .entity(error)
                .type(MediaType.APPLICATION_JSON)
                .build();
    }

        // Reject if device is disabled
        if ("MAINTENANCE".equalsIgnoreCase(sensor.getStatus())) {
            throw new SensorUnavailableException("Sensor " + sensorId + " is in maintenance mode and cannot accept readings.");
        }

        // Auto-fill generated properties
        reading.setId(DataStore.nextReadingId());
        reading.setTimestamp(System.currentTimeMillis()); // Record exact time of reading

        // Save the new reading
        DataStore.addReading(sensorId, reading);

        // Sync latest value to parent device
        sensor.setCurrentValue(reading.getValue());

        // Build response with Location header
        URI location = URI.create("/api/v1/sensors/" + sensorId + "/readings/" + reading.getId());
        return Response.created(location).entity(reading).build();
    }
}