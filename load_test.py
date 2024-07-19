import argparse
import asyncio
import aiohttp
import json
import logging
from time import perf_counter
from statistics import mean, stdev, median
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch(session, url, method, headers, payload, latencies, errors, detailed_errors):
    '''
    This function makes an HTTP GET request and records the latency.
    It appends the latency to the latencies list and any errors to the errors list.
    '''
    # Checking time with perf_counter module from time library
    # as it is more accurate than time.time()
    start_time = perf_counter()
    try:
        async with session.request(method, url, headers=headers, json=payload) as response:
            # Calculating the latency from performance counters
            latency = perf_counter() - start_time
            # Adding the latency to the latencies list
            latencies.append(latency) 
            # Checking if the response is success, 
            # o.w. add status to errors and detailed version with text to detailed_errors list
            if response.status != 200:
                errors.append(response.status)
                detailed_errors[response.status].append(await response.text())
    except Exception as e:
        errors.append(str(e))
        detailed_errors['exceptions'].append(str(e))

async def load_test(url, qps, duration, method, headers, payload, concurrency):
    '''
    This function generates requests at the specified QPS for the given duration.
    It uses asyncio.sleep to maintain the QPS rate.
    '''

    latencies = []
    errors = []
    detailed_errors = defaultdict(list)

    logger.info(f" Starting the load test for {url} with a QPS of {int(qps)} for {duration} secs.")
    # Starting a Client Session to do the load test
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(int(qps * duration)):
            if len(tasks) >= concurrency:
                await asyncio.gather(*tasks)
                tasks = []
            # Calling an instance of HTTP request
            task = fetch(session, url, method, headers, payload, latencies, errors, detailed_errors)
            tasks.append(task)
            # Use async.io sleep function to maintain the QPS
            await asyncio.sleep(1 / qps)
        # Gather all responses
        if tasks:
            await asyncio.gather(*tasks)
    logger.info(" Test complete.")
    return latencies, errors, detailed_errors

def report_results(latencies, errors, detailed_errors, output_file):
    '''
    This function calculates and writes the the metrics 
    such as mean latency, standard deviation, max, and min latencies, 
    and the number of successful and failed requests into a JSON file.
    '''

    if latencies:
        results = {
            "total_requests": len(latencies) + len(errors),
            "successful_requests": len(latencies),
            "failed_requests": len(errors),
            "mean_latency": round(mean(latencies), 4),
            "median_latency": round(median(latencies), 4),
            "stddev_latency": round(stdev(latencies), 4),
            "max_latency": round(max(latencies), 4),
            "min_latency": round(min(latencies), 4),
            "90th_percentile_latency": round(sorted(latencies)[int(len(latencies) * 0.9)], 4),
            "detailed_errors": dict(detailed_errors)
        }
    else:
        results = {
            "total_requests": len(errors),
            "successful_requests": 0,
            "failed_requests": len(errors),
            "message": "No successful requests.",
            "detailed_errors": dict(detailed_errors)
        }

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    
    logger.info(f" Results written to {output_file}")

def main():
    # Parsing the arguments such as url to do load test, qps, and the duration for the test
    parser = argparse.ArgumentParser(description='HTTP Load Testing Tool')
    parser.add_argument('url', type=str, help='URL to load test')
    parser.add_argument('--qps', type=float, default=1, help='Queries per second')
    parser.add_argument('--duration', type=int, default=10, help='Duration of the test in seconds')
    parser.add_argument('--method', type=str, default='GET', help='HTTP method to use')
    parser.add_argument('--headers', type=json.loads, default='{}', help='HTTP headers as JSON string')
    parser.add_argument('--payload', type=json.loads, default='{}', help='HTTP payload as JSON string')
    parser.add_argument('--output', type=str, default='results.json', help='Output file for results')
    parser.add_argument('--concurrency', type=int, default=1, help='Number of concurrent requests')


    args = parser.parse_args()

    url = args.url
    qps = args.qps
    duration = args.duration
    method = args.method.upper()
    headers = args.headers
    payload = args.payload
    output_file = args.output
    concurrency = args.concurrency
    
    # Run asynchronous functions of load testing
    latencies, errors, detailed_errors = asyncio.run(load_test(url, qps, duration, method, headers, payload, concurrency))    
    # Reporting results
    report_results(latencies, errors, detailed_errors, output_file)

if __name__ == '__main__':
    main()
