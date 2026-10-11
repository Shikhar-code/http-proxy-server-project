# HTTP Proxy Server

A multithreaded HTTP proxy server developed in Python as part of a Computer Networks mini-project.

The proxy acts as an intermediary between a client and a web server. It receives HTTP requests, forwards them to the destination server, and sends the responses back to the client.

The project demonstrates TCP socket programming, multithreading, HTTP communication, caching, access control, and network performance measurement.

## Features

- **HTTP Request Forwarding:** Receives HTTP requests and forwards them to destination web servers.
- **Multithreading:** Handles multiple client connections using Python threads.
- **Response Caching:** Stores eligible HTTP GET responses in memory for 60 seconds to reduce repeated requests.
- **Cache-Control Handling:** Avoids caching responses containing restrictive caching headers and requests containing authentication or cookie headers.
- **Domain Blocking:** Restricts access to domains specified in `blocked_domains.txt`.
- **Request Logging:** Records client addresses, destination hosts, requested resources, and timestamps.
- **Error Handling:** Returns HTTP error responses for invalid requests, blocked websites, unreachable servers, and timeouts.
- **Performance Testing:** Measures average latency and throughput for direct and proxied HTTP requests.

## Technologies Used

- Python 3
- TCP/IP sockets
- HTTP/1.0 and HTTP/1.1 request handling
- Python `threading` module
- Python standard libraries

No third-party Python packages are required.

## Project Structure

```text
proxy_server/
├── proxy.py
├── cache.py
├── performance_test.py
├── blocked_domains.txt
├── test_site/
│   └── index.html
├── tests/
│   └── no_store_test.py
├── .gitignore
└── README.md
```

**File descriptions:**

- `proxy.py` — Main proxy server, request forwarding, client handling, access control, logging, and error responses.
- `cache.py` — Thread-safe in-memory response cache with expiration.
- `performance_test.py` — Compares direct and proxied HTTP request performance.
- `blocked_domains.txt` — Contains domains that the proxy should block.
- `test_site/` — Simple local website used for testing.
- `tests/no_store_test.py` — Local server used to verify cache-control behavior.

## How the Proxy Works

```text
         HTTP Client
              |
              v
        Proxy Server
        (Port 8080)
              |
       Check Blocklist
              |
        Check Cache
              |
       +------+------+
       |             |
   Cache Hit     Cache Miss
       |             |
       |       Destination Server
       |             |
       |       Receive Response
       |             |
       |       Cache if Allowed
       |             |
       +------+------+
              |
              v
         HTTP Client
```

Each accepted client connection is handled by a separate thread. The proxy checks whether the destination is blocked and whether a cached response exists before contacting the destination server.

## How to Run

### 1. Start the Proxy Server

Open a terminal in the project directory and run:

```bash
python proxy.py
```

The proxy listens on:

```text
127.0.0.1:8080
```

### 2. Start the Local Test Website

In another terminal, run:

```bash
python -m http.server 9000 --bind 127.0.0.1 --directory test_site
```

### 3. Send an HTTP Request Through the Proxy

Open a third terminal:

```bash
curl.exe -i --proxy http://127.0.0.1:8080 --noproxy "nothing.invalid" http://127.0.0.1:9000/
```

The proxy should forward the request and return the local test webpage.

The `curl.exe` examples are intended for Windows.

## Testing

### Response Caching

Send the same GET request twice.

The first request should produce a `CACHE MISS`. If the response is eligible for caching, the second request should produce a `CACHE HIT`.

Cached responses expire after 60 seconds.

### Domain Blocking

Add a domain name to `blocked_domains.txt`, with one domain per line.

For example:

```text
example.com
```

Requests to blocked domains should receive:

```text
HTTP/1.1 403 Forbidden
```

### Cache-Control Testing

Run the dedicated test server:

```bash
python tests/no_store_test.py
```

It serves responses with:

```text
Cache-Control: no-store
```

Repeated requests through the proxy should not produce a cache hit.

### Performance Testing

Start the proxy and run:

```bash
python performance_test.py
```

The benchmark compares direct HTTP requests with requests forwarded through the proxy over 10 trials.

It reports:

- Average direct request latency
- Average proxied request latency
- Average latency difference
- Direct throughput
- Proxied throughput

Results depend on network conditions, the destination server, and the testing environment.

## Error Handling

The proxy includes handling for common HTTP and networking problems.

| HTTP Status | Description |
|---|---|
| 400 Bad Request | Invalid request or destination information |
| 403 Forbidden | Domain blocked by the proxy |
| 408 Request Timeout | Client request timeout, where applicable |
| 501 Not Implemented | Unsupported HTTP method |
| 502 Bad Gateway | Destination server cannot be reached |
| 504 Gateway Timeout | Destination server response timeout |

## Limitations

- Supports HTTP GET and HEAD requests, but not other request methods.
- Does not support HTTPS tunneling through the CONNECT method.
- Uses an in-memory cache that is cleared when the proxy stops.
- Uses a fixed cache expiration time of 60 seconds.
- Is intended for small-scale demonstration rather than production deployment.
- Does not guarantee correct handling of requests whose HTTP headers arrive in multiple TCP reads.

## Conclusion

This project demonstrates the fundamental working of an HTTP forward proxy using Python socket programming. It combines request forwarding, concurrent client handling, caching, domain filtering, logging, and performance measurement in a single application.