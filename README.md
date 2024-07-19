# HTTP Load Testing Tool

This is a Python-based HTTP load testing tool that allows you to test the performance of a web server by simulating multiple requests. The tool supports various HTTP methods, custom headers, payloads, and concurrency levels. It reports detailed latency statistics and error rates.

## Features

- Supports different HTTP methods (GET, POST, PUT, DELETE, etc.)
- Custom headers and payloads
- Concurrency control
- Detailed latency and error reporting
- Output results to a JSON file
- Progress logging

## Prerequisites

Only prerequisite library is `aiohttp` that handles asynchronous HTTP requests. It is a part of the Docker image, therefore you don't need to install that separately. 

## Usage

### Pull the Docker Image

```
docker pull aagoksoy/http-load-tester:latest
```

### Run the Docker Container

Start the container and open an interactive shell:

```
docker run -it --rm -v $(pwd):/app aagoksoy/http-load-tester:latest
```

### Run the Load Test

Run the script from the command line with the required arguments.

```
python load_test.py URL --qps QPS --duration DURATION --method METHOD --headers HEADERS --payload PAYLOAD --output OUTPUT --concurrency CONCURRENCY
```

- URL (required): The URL to load test.
- --qps (optional): Queries per second (default: 1).
- --duration (optional): Duration of the test in seconds (default: 10).
- --method (optional): HTTP method to use (default: GET).
- --headers (optional): HTTP headers as a JSON string (default: {}).
- --payload (optional): HTTP payload as a JSON string (default: {}).
- --output (optional): Output file for results (default: results.json).
- --concurrency (optional): Number of concurrent requests (default: 1).

## Examples

### Basic GET Request

```
python load_test.py http://example.com --qps 5 --duration 10 --output results.json --concurrency 10
```

This command will load test http://example.com with 5 queries per second for 10 seconds, write the results to results.json, and use 10 concurrent requests.

### POST Request with JSON Payload and Headers

```
python load_test.py http://example.com --qps 5 --duration 10 --method POST --headers '{"Content-Type": "application/json", "Authorization": "Bearer <token>"}' --payload '{"username": "exampleuser", "password": "examplepassword"}' --output results.json --concurrency 10
```

This command will load test http://example.com with a POST request, sending custom headers and a JSON payload. It will use 5 queries per second for 10 seconds, write the results to results.json, and use 10 concurrent requests.

### Example Headers

__1. Content-Type Header:__ Specifies the media type of the resource.

```
{
    "Content-Type": "application/json"
}
```

__2. Authorization Header:__ Used for sending credentials.

```
{
    "Authorization": "Bearer <token>"
}
```

__3. Custom Headers:__ Headers that are specific to your application.

```
{
    "X-Custom-Header": "value"
}
```

### Example Payloads

__JSON Payload:__
```
{
    "username": "exampleuser",
    "password": "examplepassword"
}
```
__Form Data Payload:__

```
{
    "field1": "value1",
    "field2": "value2"
}
```
## Output

The results will be written to the specified output file in JSON format. Here is an example of what the results.json file might look like:

```
{
    "total_requests": 50,
    "successful_requests": 48,
    "failed_requests": 2,
    "mean_latency": 0.1234,
    "median_latency": 0.121,
    "stddev_latency": 0.0123,
    "max_latency": 0.1456,
    "min_latency": 0.1012,
    "90th_percentile_latency": 0.135,
    "detailed_errors": {
        "500": ["Internal Server Error"],
        "exceptions": ["Some exception message"]
    }
}
```

## Logging

The script provides logging to give you real-time feedback on the progress of the load test. The results of the test, including detailed error logs, are saved in the specified output file.

