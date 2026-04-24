# "Smart Campus" Sensor & Room Management API

## 1. Overview
The "Smart Campus" API is a robust, highly-available RESTful web service built with Java and JAX-RS (Jakarta RESTful Web Services). It is designed to act as the backend infrastructure for a university's Smart Campus initiative, managing thousands of physical rooms and a diverse array of hardware sensors (e.g., CO2 monitors, occupancy trackers, and temperature sensors). 

The platform features strict validation constraints (e.g., preventing the deletion of rooms with active sensors), sub-resource locators for maintaining telemetry history logs, dynamic filtering for hardware retrieval, and an advanced error-handling architecture that converts application exceptions into semantically accurate HTTP responses (such as 409 Conflict, 422 Unprocessable Entity, and 403 Forbidden).

---

## 2. Build & Launch Instructions

### Prerequisites
- JDK 11 or higher
- Apache Maven (3.6+)
- A Servlet Container (e.g., Apache Tomcat 9/10, or GlassFish)

### Building the Project
1. Clone the repository and navigate to the project root directory where the \pom.xml\ is located.
2. Run the following Maven command to compile the application and package it into a \.war\ file:
   \\\ash
   mvn clean package
   \\\
3. A \.war\ file (e.g., \SmartCampusAPI.war\) will be generated inside the \	arget/\ directory.

### Deploying the Server
1. Copy the generated \.war\ file from the \	arget/\ directory.
2. Paste it into the \webapps/\ directory of your local Tomcat installation.
3. Start the Tomcat server. (e.g., by running \in/startup.bat\ on Windows or \in/startup.sh\ on Unix/macOS).
4. By default, the application will be hosted at:
   \http://localhost:8080/SmartCampusAPI/api/v1\

---

## 3. Sample API Interactions (cURL)

Here are five \curl\ commands demonstrating interactions with different parts of the API:

**1. Create a New Room (POST)**
\\\ash
curl -X POST http://localhost:8080/SmartCampusAPI/api/v1/rooms \
-H "Content-Type: application/json" \
-d '{"name": "Main Lecture Hall", "capacity": 250}'
\\\

**2. Retrieve All Rooms (GET)**
\\\ash
curl -X GET http://localhost:8080/SmartCampusAPI/api/v1/rooms
\\\

**3. Register a New Sensor to a Room (POST)**
\\\ash
curl -X POST http://localhost:8080/SmartCampusAPI/api/v1/sensors \
-H "Content-Type: application/json" \
-d '{"type": "CO2", "status": "ACTIVE", "roomId": "R1"}'
\\\

**4. Filter Sensors by Type (GET)**
\\\ash
curl -X GET "http://localhost:8080/SmartCampusAPI/api/v1/sensors?type=CO2"
\\\

**5. Append a New Sensor Reading (POST)**
\\\ash
curl -X POST http://localhost:8080/SmartCampusAPI/api/v1/sensors/S1/readings \
-H "Content-Type: application/json" \
-d '{"value": 412.5}'
\\\

---

## 4. Coursework Report (Conceptual Answers)

### Part 1: Service Architecture & Setup
**1.1 Default Lifecycle & Data Synchronisation:**
By default, JAX-RS resource classes are "request-scoped," meaning the runtime instantiates a completely new instance of the class for every incoming HTTP request. This prevents instance-variable contamination between users. However, because new instances are constantly interacting with the same underlying \DataStore\ (which holds static, in-memory structures), there is a significant risk of race conditions during concurrent updates. To mitigate this, our architectural decision requires the use of thread-safe components�such as \ConcurrentHashMap\ for collections and \AtomicInteger\ for unique ID generation�ensuring data parity and preventing loss across concurrent request threads.

**1.2 The "Discovery" Endpoint (HATEOAS):**
Providing Hypermedia (HATEOAS) is a hallmark of advanced RESTful design because it makes the API dynamically self-discoverable. Instead of forcing client developers to hardcode static URI routes from external documentation, HATEOAS embeds navigational transition links directly within the server's responses. This highly benefits clients as it decouples them from the API's static routing configurations; the server can seamlessly evolve, alter paths, or deprecate endpoints without breaking existing client integrations, as clients iteratively follow the dynamic links.

### Part 2: Room Management
**2.1 Returning Room IDs vs Full Objects:**
Returning only resource IDs from a collection endpoint significantly reduces the JSON payload size, preserving network bandwidth and lowering the server's serialization overhead. However, it forces the client into the "N+1 query problem," where they must make numerous subsequent HTTP requests to fetch full metadata for each room id. Conversely, returning full objects incurs a heavier initial payload size but drastically reduces total API round-trips. In IoT infrastructures with potentially thousands of queries, the choice often necessitates pagination alongside full-object delivery, striking a balance between latency and bandwidth.

**2.2 Room Deletion & Idempotency:**
Yes, the \DELETE\ operation in this API is strictly idempotent. Idempotency guarantees that issuing multiple identical requests will not change the system state beyond the application of the initial request. If a client sends a \DELETE\ request for a specific room, the server evaluates constraints (checking for orphan sensors) and removes it�returning a \204 No Content\ or \200 OK\. If the client mistakenly submits the exact same \DELETE\ request a second time, the server will return a \404 Not Found\. Despite the varying HTTP status codes, the ultimate server-side state (the room being completely absent from the collection) remains unchanged, fulfilling the strict definition of idempotency.

### Part 3: Sensor Operations & Linking
**3.1 Content-Type Mismatches & @Consumes:**
By explicitly declaring \@Consumes(MediaType.APPLICATION_JSON)\ on the POST creation method, we strictly limit the payload parser. If a client attempts to submit an incompatible format�such as \	ext/plain\ or \pplication/xml\�the JAX-RS runtime intercepts the request before it ever reaches our business logic. It automatically rejects the interaction by throwing a \NotSupportedException\ and immediately returning an HTTP \415 Unsupported Media Type\ to the client. This natively protects the backend against erratic parsing failures or malicious injection attempts hidden inside non-standard payload wrappers.

**3.2 @QueryParam Filtering vs Path Parameters:**
Query parameters (e.g., \?type=CO2\) are inherently optional, composable, and order-independent, making them vastly superior for searching and narrowing collections. In contrast, embedding parameters purely in the URL path (e.g., \/sensors/type/CO2\) rigidly dictates hierarchical identity. A structural path implies that "type CO2" is a definitive sub-resource, rather than an arbitrary characteristic dynamically filtering a broader \/sensors\ base collection. Furthermore, Query Parameters effortlessly scale�chaining multiple filters (e.g., \?type=CO2&status=ACTIVE\) is seamless natively, whereas designing nested path structures for complex AND/OR search dynamics quickly becomes unmaintainable.

### Part 4: Deep Nesting with Sub-Resources
**4.1 Architectural Benefits of Sub-Resource Locators:**
The Sub-Resource Locator pattern effectively manages scale by splitting massive, monolithic controller files (where every permutation of nested endpoints like \/sensors/{id}/readings/...\ are defined in one place) into focused, single-responsibility classes. The parent \SensorResource\ merely evaluates the routing context and dynamically delegates execution to a distinct \SensorReadingResource\ controller. This modularity prevents codebase bloat, makes individual modules independently testable, reduces cognitive load for developers reading the class structure, and intrinsically separates "hardware management logic" from "telemetry log processing."

### Part 5: Advanced Error Handling, Exception Mapping & Logging
**5.2 422 Unprocessable Entity vs 404 Not Found:**
An HTTP \404 Not Found\ semantically communicates that the requested URI endpoint (e.g., \/sensors\) entirely fails to exist on the routing table. When a client successfully POSTs to a valid endpoint but provides a syntactically correct JSON body containing an invalid internal reference (like a non-existent \
oomId\), the sever understands the content type and the request routing is completely valid. Thus, returning a \422 Unprocessable Entity\ is vastly more semantically accurate�it precisely indicates that the payload was parsable, but the domain-specific semantic instructions contained within could not be fulfilled due to logic constraint violations.

**5.4 Security Risks of Internal Stack Traces (500 Errors):**
Exposing raw Java stack traces to external API consumers is a critical cybersecurity vulnerability (Information Disclosure). It directly maps out the application's entire internal topography�displaying the exact file directories, unhandled null logic lines, specific framework names (e.g., Jersey 2.x), and underlying library components (e.g., Jackson JSON processors). Attackers scrape these stack traces to footprint the technology stack and cross-reference the leaked library coordinates against known Common Vulnerabilities and Exposures (CVEs), subsequently deploying highly targeted exploits explicitly designed for the outdated dependencies the API unintentionally exposed.

**5.5 Advantage of JAX-RS Resource Filters for Logging:**
JAX-RS filters (like \ContainerRequestFilter\ and \ContainerResponseFilter\) provide an elegant mechanism for dealing with cross-cutting concerns by decoupling logging behaviors entirely from core business logic. Inserting raw \Logger.info()\ statements into dozens of separate resource methods deeply violates the DRY (Don't Repeat Yourself) principle, heavily clutters the application codebase, and guarantees human error when developers eventually forget to append the logging statements to newly created endpoints. JAX-RS filters intercept the routing globally at the container tier�guaranteeing 100% comprehensive observability of all inbound and outbound traffic independently.
