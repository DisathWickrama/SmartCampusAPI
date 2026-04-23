package com.smartcampus.resource;

import com.smartcampus.dao.DataStore;
import com.smartcampus.exception.LinkedResourceNotFoundException;
import com.smartcampus.model.ErrorMessage;
import com.smartcampus.model.Room;
import com.smartcampus.model.Sensor;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.net.URI;
import java.util.List;
import java.util.stream.Collectors;

@Path("/sensors")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class SensorResource {

    // Get devices, optionally filtered by type
    @GET
    public List<Sensor> fetchCampusSensors(@QueryParam("type") String type) {
        if (type == null || type.isEmpty()) {
            return DataStore.sensors;
        }
        // Implement type filtering
        return DataStore.sensors.stream()
                .filter(s -> s.getType().equalsIgnoreCase(type))
                .collect(Collectors.toList());
    }

    // Add new device (validentifierentifierates location existence)
    @POST
    public Response installNewSensor(Sensor sensor) {
        // Validentifierentifierate that the specified location exists
        Room room = DataStore.rooms.stream()
                .filter(r -> r.getId().equals(sensor.getRoomId()))
                .findFirst()
                .orElse(null);
        if (room == null) {
            throw new LinkedResourceNotFoundException("Room with ID " + sensor.getRoomId() + " does not exist.");
        }

        // Assign generated device ID
        sensor.setId(DataStore.nextSensorId());
        DataStore.sensors.add(sensor);

        // Add device reference to the location
        room.getSensorIds().add(sensor.getId());

        URI location = URI.create("/api/v1/sensors/" + sensor.getId());
        return Response.created(location).entity(sensor).build();
    }

    // Get individentifierentifierual device details
    @GET
    @Path("/{sensorId}")
    public Response fetchSensorDetails(@PathParam("sensorId") String sensorId) {
        Sensor sensor = DataStore.sensors.stream()
                .filter(s -> s.getId().equals(sensorId))
                .findFirst()
                .orElse(null);
        if (sensor == null) {
            ErrorMessage error = new ErrorMessage(404, "SENSOR_NOT_FOUND", "Sensor with ID " + sensorId + " does not exist.");
            return Response.status(Response.Status.NOT_FOUND).entity(error).build();
        }
        return Response.ok(sensor).build();
    }

    // Forward to SensorReadingResource
    @Path("/{sensorId}/readings")
    public SensorReadingResource delegateToReadingResource(@PathParam("sensorId") String sensorId) {
        return new SensorReadingResource(sensorId);
    }
}