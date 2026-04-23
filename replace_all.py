import os
import glob
import re

replacements = {
    "// Concurrency-safe generators for building unique textual IDs": "// Thread-safe ID generators",
    "// Bootstrapping the data context": "// Initialize baseline dummy data",
    "// Generate initial campus locations": "// Create starting room entries",
    "// Setup base campus hardware": "// Initialize default sensor devices",
    "// Link the hardware to their respective locations": "// Connect sensors to rooms",
    "// Set up blank history arrays for each monitor": "// Prepare empty reading lists for sensors",
    "// Add dummy historical data readings": "// Insert sample data points",
    "// 422 Unprocessable Entity": "// HTTP 422 Unprocessable Entity",
    "// Properties accessors (Getters / Setters)": "// Accessor methods (get/set)",
    "// Unique reading event ID (UUID recommended)": "// Distinct reading ID",
    "// Epoch time (ms) when the reading was captured": "// Timestamp in milliseconds",
    "// The actual metric value recorded by the hardware": "// Recorded metric value",
    "// Basic Application Identity": "// Core API info",
    "// Developer contact details Information": "// Support contact details",
    "// System endpoints and routes Directory": "// Application routes",
    "// Retrieve entire campus room catalog": "// Get all configured rooms",
    "// Fetch details of an individual room by passing its ID in the URL": "// Load room details by ID",
    "// Endpoint to register a new room into the system": "// Register a new room",
    "// Allocate unique ID dynamically": "// Assign a new unique identifier",
    "// Remove a room (Validation: Fails with 409 if hardware sensors are still mapped to it)": "// Delete room (must be empty of sensors)",
    "// State passed down from the parent path": "// Context provided by parent resource",
    "// Fetch full history log": "// Retrieve all historical readings",
    "// Append a new data metric, altering parent state": "// Add a reading and update sensor state",
    "// Retrieve associated sensor": "// Fetch the parent sensor",
    "// Block requests if hardware is inactive": "// Reject if sensor is disabled",
    "// Auto-assign properties": "// Auto-fill generated properties",
    "// Set time": "// Record exact time of reading",
    "// Commit to datastore": "// Save the new reading",
    "// Critical state synchronisation (side-effect)": "// Sync latest value to parent sensor",
    "// Formulate correct URI for 201 Created Header": "// Build response with Location header",
    "// Retrieve sensor list with optional query param filtering": "// Get sensors, optionally filtered by type",
    "// Apply requested filter logic": "// Implement type filtering",
    "// Register new hardware (Enforces validation on the parent room ID)": "// Add new sensor (validates room existence)",
    "// Confirm linked room matches an active location": "// Validate that the specified room exists",
    "// Set system identifier": "// Assign generated sensor ID",
    "// Bind sensor ID to the parent room array": "// Add sensor reference to the room",
    "// Fetch detailed metadata for one sensor": "// Get individual sensor details",
    "// Delegate reading endpoints to Sub-Resource Locator": "// Forward to SensorReadingResource"
}

count = 0
for filepath in glob.glob("src/main/java/**/*.java", recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = content
    for old, new in replacements.items():
        modified = modified.replace(old, new)
        
    if modified != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified)
        print(f"Updated {filepath}")
        count += 1
print(f"Total files formatted: {count}")
