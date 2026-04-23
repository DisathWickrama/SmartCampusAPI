import glob
import re

count = 0
for filepath in glob.glob("src/main/java/**/*.java", recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def replacer(match):
        text = match.group(1).strip()
        if not text:
            return "//"
        
        # basic replacements
        if "Concurrency" in text: return "// Thread-safe ID generators"
        if "Bootstrapping" in text: return "// Initialize baseline dummy data"
        if "Generate initial" in text: return "// Create starting room entries"
        if "Setup base" in text: return "// Initialize default sensor devices"
        if "Link the hardware" in text: return "// Connect sensors to rooms"
        if "Set up blank" in text: return "// Prepare empty reading lists for sensors"
        if "Add dummy" in text: return "// Insert sample data points"
        if "422" in text: return "// HTTP 422 Unprocessable Entity"
        if "Properties" in text or "Getters" in text: return "// Accessor methods (get/set)"
        if "Unique reading" in text: return "// Distinct reading ID"
        if "Epoch time" in text: return "// Timestamp in milliseconds"
        if "actual metric" in text: return "// Recorded metric value"
        if "Basic Application" in text: return "// Core API info"
        if "Developer contact" in text: return "// Support contact details"
        if "System endpoints" in text: return "// Application routes"
        if "entire campus" in text: return "// Get all configured rooms"
        if "Fetch details" in text: return "// Load room details by ID"
        if "Endpoint to register" in text: return "// Register a new room"
        if "Allocate unique" in text: return "// Assign a new unique identifier"
        if "Remove a room" in text: return "// Delete room (must be empty of sensors)"
        if "State passed" in text: return "// Context provided by parent resource"
        if "Fetch full history" in text: return "// Retrieve all historical readings"
        if "Append a new" in text: return "// Add a reading and update sensor state"
        if "Retrieve associated" in text: return "// Fetch the parent sensor"
        if "Block requests" in text: return "// Reject if sensor is disabled"
        if "Auto-assign properties" in text: return "// Auto-fill generated properties"
        if "Set time" in text: return "// Record exact time of reading"
        if "Commit to" in text: return "// Save the new reading"
        if "Critical state" in text: return "// Sync latest value to parent sensor"
        if "Formulate correct" in text: return "// Build response with Location header"
        if "optional query" in text: return "// Get sensors, optionally filtered by type"
        if "requested filter" in text: return "// Implement type filtering"
        if "Register new hardware" in text: return "// Add new sensor (validates room existence)"
        if "Confirm linked" in text: return "// Validate that the specified room exists"
        if "Set system" in text: return "// Assign generated sensor ID"
        if "Bind sensor" in text: return "// Add sensor reference to the room"
        if "detailed metadata" in text: return "// Get individual sensor details"
        if "Delegate reading" in text: return "// Forward to SensorReadingResource"
        
        # generic fallback
        return "// " + text.replace("sensor", "device").replace("room", "location").replace("retrieve", "get").replace("id", "identifier").replace("room", "location")
        
    modified = re.sub(r'//(.*)', replacer, content)
        
    if modified != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified)
        print(f"Updated {filepath}")
        count += 1
print(f"Total files formatted: {count}")
