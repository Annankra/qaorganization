--- Performance Load Test Plan ---
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Define thresholds
const responseTimeThreshold = 2000; // 2 seconds
const errorRateThreshold = 0.01; // 1%

// Custom metrics
const errorRate = new Rate('errors');

export const options = {
    stages: [
        { duration: '1m', target: 10 }, // Ramp-up to 10 users over 1 minute
        { duration: '3m', target: 10 }, // Stay at 10 users for 3 minutes
        { duration: '1m', target: 0 },  // Ramp-down to 0 users over 1 minute
    ],
    thresholds: {
        http_req_duration: [`p(95)<${responseTimeThreshold}`], // 95% of requests should be below 2 seconds
        errors: [`rate<${errorRateThreshold}`], // Error rate should be below 1%
    },
};

export default function () {
    const url = 'https://your-application.com/api/password-reset';
    const payload = JSON.stringify({
        email: 'user@example.com',
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const res = http.post(url, payload, params);

    // Check if the response was successful
    const success = check(res, {
        'is status 200': (r) => r.status === 200,
        'response time < 2s': (r) => r.timings.duration < responseTimeThreshold,
    });

    // Record error rate
    errorRate.add(!success);

    sleep(1);
}
```

--- Execution Results ---
Load Test FAILED:
Stdout:
/\      Grafana   /‾‾/  
    /\  /  \     |\  __   /  /   
   /  \/    \    | |/ /  /   ‾‾\ 
  /          \   |   (  |  (‾)  |
 / __________ \  |_|\_\  \_____/ 

     execution: local
        script: /var/folders/05/0z812bxj2lz4n79z43jkk1y00000gp/T/tmpr16r1yys.js
        output: -

     scenarios: (100.00%) 1 scenario, 10 max VUs, 5m30s max duration (incl. graceful stop):
              * default: Up to 10 looping VUs for 5m0s over 3 stages (gracefulRampDown: 30s, gracefulStop: 30s)


running (0m01.0s), 01/10 VUs, 0 complete and 0 interrupted iterations
default   [   0% ] 01/10 VUs  0m01.0s/5m00.0s

running (0m02.0s), 01/10 VUs, 1 complete and 0 interrupted iterations
default   [   1% ] 01/10 VUs  0m02.0s/5m00.0s

running (0m03.0s), 01/10 VUs, 2 complete and 0 interrupted iterations
default   [   1% ] 01/10 VUs  0m03.0s/5m00.0s

running (0m04.0s), 01/10 VUs, 3 complete and 0 interrupted iterations
default   [   1% ] 01/10 VUs  0m04.0s/5m00.0s

running (0m05.0s), 01/10 VUs, 4 complete and 0 interrupted iterations
default   [   2% ] 01/10 VUs  0m05.0s/5m00.0s

running (0m06.0s), 01/10 VUs, 5 complete and 0 interrupted iterations
default   [   2% ] 01/10 VUs  0m06.0s/5m00.0s

running (0m07.0s), 02/10 VUs, 5 complete and 0 interrupted iterations
default   [   2% ] 02/10 VUs  0m07.0s/5m00.0s

running (0m08.0s), 02/10 VUs, 7 complete and 0 interrupted iterations
default   [   3% ] 02/10 VUs  0m08.0s/5m00.0s

running (0m09.0s), 02/10 VUs, 8 complete and 0 interrupted iterations
default   [   3% ] 02/10 VUs  0m09.0s/5m00.0s

running (0m10.0s), 02/10 VUs, 10 complete and 0 interrupted iterations
default   [   3% ] 02/10 VUs  0m10.0s/5m00.0s

running (0m11.0s), 02/10 VUs, 12 complete and 0 interrupted iterations
default   [   4% ] 02/10 VUs  0m11.0s/5m00.0s

running (0m12.0s), 02/10 VUs, 14 complete and 0 interrupted iterations
default   [   4% ] 02/10 VUs  0m12.0s/5m00.0s

running (0m13.0s), 02/10 VUs, 16 complete and 0 interrupted iterations
default   [   4% ] 02/10 VUs  0m13.0s/5m00.0s

running (0m14.0s), 03/10 VUs, 17 complete and 0 interrupted iterations
default   [   5% ] 03/10 VUs  0m14.0s/5m00.0s

running (0m15.0s), 03/10 VUs, 20 complete and 0 interrupted iterations
default   [   5% ] 03/10 VUs  0m15.0s/5m00.0s

running (0m16.0s), 03/10 VUs, 23 complete and 0 interrupted iterations
default   [   5% ] 03/10 VUs  0m16.0s/5m00.0s

running (0m17.0s), 03/10 VUs, 25 complete and 0 interrupted iterations
default   [   6% ] 03/10 VUs  0m17.0s/5m00.0s

running (0m18.0s), 03/10 VUs, 28 complete and 0 interrupted iterations
default   [   6% ] 03/10 VUs  0m18.0s/5m00.0s

running (0m19.0s), 03/10 VUs, 30 complete and 0 interrupted iterations
default   [   6% ] 03/10 VUs  0m19.0s/5m00.0s

running (0m20.0s), 03/10 VUs, 33 complete and 0 interrupted iterations
default   [   7% ] 03/10 VUs  0m20.0s/5m00.0s

running (0m21.0s), 04/10 VUs, 36 complete and 0 interrupted iterations
default   [   7% ] 04/10 VUs  0m21.0s/5m00.0s

running (0m22.0s), 04/10 VUs, 39 complete and 0 interrupted iterations
default   [   7% ] 04/10 VUs  0m22.0s/5m00.0s

running (0m23.0s), 04/10 VUs, 43 complete and 0 interrupted iterations
default   [   8% ] 04/10 VUs  0m23.0s/5m00.0s

running (0m24.0s), 04/10 VUs, 47 complete and 0 interrupted iterations
default   [   8% ] 04/10 VUs  0m24.0s/5m00.0s

running (0m25.0s), 04/10 VUs, 50 complete and 0 interrupted iterations
default   [   8% ] 04/10 VUs  0m25.0s/5m00.0s

running (0m26.0s), 04/10 VUs, 53 complete and 0 interrupted iterations
default   [   9% ] 04/10 VUs  0m26.0s/5m00.0s

running (0m27.0s), 05/10 VUs, 57 complete and 0 interrupted iterations
default   [   9% ] 05/10 VUs  0m27.0s/5m00.0s

running (0m28.0s), 05/10 VUs, 61 complete and 0 interrupted iterations
default   [   9% ] 05/10 VUs  0m28.0s/5m00.0s

running (0m29.0s), 05/10 VUs, 66 complete and 0 interrupted iterations
default   [  10% ] 05/10 VUs  0m29.0s/5m00.0s

running (0m30.0s), 05/10 VUs, 69 complete and 0 interrupted iterations
default   [  10% ] 05/10 VUs  0m30.0s/5m00.0s

running (0m31.0s), 05/10 VUs, 74 complete and 0 interrupted iterations
default   [  10% ] 05/10 VUs  0m31.0s/5m00.0s

running (0m32.0s), 05/10 VUs, 78 complete and 0 interrupted iterations
default   [  11% ] 05/10 VUs  0m32.0s/5m00.0s

running (0m33.0s), 05/10 VUs, 83 complete and 0 interrupted iterations
default   [  11% ] 05/10 VUs  0m33.0s/5m00.0s

running (0m34.0s), 06/10 VUs, 87 complete and 0 interrupted iterations
default   [  11% ] 06/10 VUs  0m34.0s/5m00.0s

running (0m35.0s), 06/10 VUs, 92 complete and 0 interrupted iterations
default   [  12% ] 06/10 VUs  0m35.0s/5m00.0s

running (0m36.0s), 06/10 VUs, 96 complete and 0 interrupted iterations
default   [  12% ] 06/10 VUs  0m36.0s/5m00.0s

running (0m37.0s), 06/10 VUs, 102 complete and 0 interrupted iterations
default   [  12% ] 06/10 VUs  0m37.0s/5m00.0s

running (0m38.0s), 06/10 VUs, 107 complete and 0 interrupted iterations
default   [  13% ] 06/10 VUs  0m38.0s/5m00.0s

running (0m39.0s), 06/10 V
... [Output Truncated for Brevity] ...
Error: None

--- Performance Bottleneck Analysis ---
Based on the provided performance metrics from the load test, here is an analysis of the system's performance, potential bottlenecks, scalability issues, and suggestions for optimization:

### Analysis:

1. **Test Setup and Execution:**
   - The load test is configured to run with a maximum of 10 Virtual Users (VUs) over a duration of 5 minutes, split into 3 stages with a graceful ramp-down and stop of 30 seconds each.
   - The test failed, but no specific error message is provided in the output, which suggests the failure might be related to unmet performance criteria or a timeout.

2. **Performance Metrics:**
   - The test ran for 39 seconds before the output was truncated.
   - The number of VUs started at 1 and gradually increased, reaching 6 VUs by the 39th second.
   - The percentage of test completion was at 13% when the output was truncated, indicating that the test was still in its early stages.

3. **Potential Bottlenecks:**
   - **Scalability Limitations:** The system might be struggling to handle the gradual increase in VUs, as seen by the slow ramp-up and the test failure. This could indicate issues with resource allocation or system capacity.
   - **Throughput and Latency:** The number of completed iterations per second seems low. This could be due to high response times or processing delays, which might be causing a bottleneck.
   - **Concurrency Handling:** The system might not be optimized for handling concurrent users effectively, leading to performance degradation as more VUs are introduced.

4. **Scalability Issues:**
   - The system's ability to scale with increased load is questionable, given the slow ramp-up and early failure. This could be due to limitations in the backend infrastructure, such as database performance, network bandwidth, or server CPU/memory constraints.

5. **Regression Indicators:**
   - Without historical data or previous test results, it's challenging to identify regressions. However, the test failure and low iteration completion rate suggest a potential performance regression compared to expected outcomes.

### Suggestions for Optimization:

1. **Resource Allocation:**
   - Ensure that the system has sufficient resources (CPU, memory, network bandwidth) to handle the expected load. Consider scaling up or out if necessary.

2. **Load Balancing:**
   - Implement or optimize load balancing strategies to distribute the load evenly across servers or instances, preventing any single point from becoming a bottleneck.

3. **Database Optimization:**
   - Analyze database queries for inefficiencies and optimize them. Consider indexing, query caching, or database sharding to improve performance.

4. **Code Profiling:**
   - Profile the application code to identify slow functions or methods that could be optimized for better performance.

5. **Asynchronous Processing:**
   - Where possible, implement asynchronous processing for tasks that do not require immediate completion, reducing the load on the system during peak times.

6. **Caching Strategies:**
   - Implement caching mechanisms (e.g., in-memory caches like Redis or Memcached) to reduce the load on databases and improve response times.

7. **Monitoring and Alerts:**
   - Set up comprehensive monitoring and alerting to quickly identify and address performance issues as they arise.

By addressing these areas, you can enhance the system's performance, improve scalability, and potentially resolve the issues that led to the load test failure.