import os
import glob

replacements = {
    "// Concurrency-safe data structures for mocked database": "// Thread-safe maps acting as an in-memory database",
    "// Bootstrapping the initial system state": "// Initialize preliminary system data",
    "// Generate initial room definitions": "// Create default room objects",
    "// Setup base sensors": "// Initialize default sensors",
    "// Link the hardware to environments": "// Associate sensors with respective rooms",
    "// Set up blank telemetry histories": "// Initialize empty arrays for sensor data",
    "// Seed some historical metrics": "// Add dummy historical data readings",
    "// Getters and Setters": "// Properties accessors (Getters / Setters)",
    "// Or UUID": "// Unique identifier",
    "// epoch ms": "// Timestamp in epoch milliseconds",
    "// Reading metric": "// Recorded value",
    "// Basic Application Profile": "// Core API metadata",
    "// Support Contact": "// Developer contact details",
    "// Available Endpoints": "// System endpoints and routes",
    "// Retrieve entire catalog of rooms": "// Get a list of all existing rooms",
    "// Fetch details of a distinct room": "// Retrieve information for a single room",
    "// Endpoint to register a fresh room": "// Route for generating new rooms",
    "// Allocate unique identifier": "// Assign a distinct ID",
    "// Remove a room (must be empty)": "// Delete room if no associated hardware",
    "// State passed down from SensorResource parent": "// Inherited context from parent SensorResource",
    "// Fetch full history log for sensor": "// Get complete telemetry records for this hardware",
    "// Append a new data point": "// Add a fresh telemetry record",
    "// Retrieve associated hardware": "// Evaluate parent sensor status",
    "// Block requests if sensor is deactivated": "// Prevent insertions on inactive hardware",
    "// Auto-assign system attributes": "// Populate system-defined fields automatically",
    "// Set actual receipt time": "// Register system time of receipt",
    "// Commit to data store": "// Persist new value in memory",
    "// Critical step: Sync the cached latest reading value": "// Update the sensor's most recent data point",
    "// Formulate create response with URI": "// Build and return HTTP 201 response",
    "// Retrieve sensors, filterable by type": "// Get all sensors, with optional type filtering",
    "// Apply requested filter if present": "// Filter by type if parameter is provided",
    "// Register new hardware component": "// Add a newly deployed sensor",
    "// Confirm linked room exists": "// Verify the referenced room is valid",
    "// Set system generated ID and defaults": "// Initialize primary key and default settings",
    "// Bind sensor to its environment": "// Attach the equipment to designated location",
    "// Delegate reading operations to sub-resource route": "// Pass execution to child resource for data points",
    "// Fetch detailed payload for a specific sensor": "// Retrieve detailed information for one sensor",
    "// Logs method + URI for requests, status code for responses": "// Automatically log HTTP interactions to console"
}

for filepath in glob.glob("src/main/java/**/*.java", recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = content
    for old_str, new_str in replacements.items():
        modified = modified.replace(old_str, new_str)
        
    if modified != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified)
        print(f"Updated {filepath}")
