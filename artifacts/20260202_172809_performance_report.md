--- Performance Load Test Plan ---
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export let errorRate = new Rate('errors');

export let options = {
    stages: [
        { duration: '1m', target: 50 }, // ramp-up to 50 users
        { duration: '3m', target: 50 }, // stay at 50 users
        { duration: '1m', target: 100 }, // ramp-up to 100 users
        { duration: '3m', target: 100 }, // stay at 100 users
        { duration: '1m', target: 0 }, // ramp-down to 0 users
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
        errors: ['rate<0.01'], // error rate should be less than 1%
    },
};

export default function () {
    const url = 'https://your-api-domain.com/login';
    const payload = JSON.stringify({
        username: 'testuser',
        password: 'testpassword',
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    let res = http.post(url, payload, params);

    const result = check(res, {
        'is status 200': (r) => r.status === 200,
        'response time < 500ms': (r) => r.timings.duration < 500,
    });

    errorRate.add(!result);

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
        script: /var/folders/05/0z812bxj2lz4n79z43jkk1y00000gp/T/tmp4ohemtpw.js
        output: -

     scenarios: (100.00%) 1 scenario, 100 max VUs, 9m30s max duration (incl. graceful stop):
              * default: Up to 100 looping VUs for 9m0s over 5 stages (gracefulRampDown: 30s, gracefulStop: 30s)


running (0m01.0s), 001/100 VUs, 0 complete and 0 interrupted iterations
default   [   0% ] 001/100 VUs  0m01.0s/9m00.0s

running (0m02.0s), 002/100 VUs, 0 complete and 0 interrupted iterations
default   [   0% ] 002/100 VUs  0m02.0s/9m00.0s

running (0m03.0s), 003/100 VUs, 2 complete and 0 interrupted iterations
default   [   1% ] 003/100 VUs  0m03.0s/9m00.0s

running (0m04.0s), 004/100 VUs, 3 complete and 0 interrupted iterations
default   [   1% ] 004/100 VUs  0m04.0s/9m00.0s

running (0m05.0s), 005/100 VUs, 6 complete and 0 interrupted iterations
default   [   1% ] 005/100 VUs  0m05.0s/9m00.0s

running (0m06.0s), 005/100 VUs, 9 complete and 0 interrupted iterations
default   [   1% ] 005/100 VUs  0m06.0s/9m00.0s

running (0m07.0s), 006/100 VUs, 14 complete and 0 interrupted iterations
default   [   1% ] 006/100 VUs  0m07.0s/9m00.0s

running (0m08.0s), 007/100 VUs, 17 complete and 0 interrupted iterations
default   [   1% ] 007/100 VUs  0m08.0s/9m00.0s

running (0m09.0s), 008/100 VUs, 23 complete and 0 interrupted iterations
default   [   2% ] 008/100 VUs  0m09.0s/9m00.0s

running (0m10.0s), 009/100 VUs, 29 complete and 0 interrupted iterations
default   [   2% ] 009/100 VUs  0m10.0s/9m00.0s

running (0m11.0s), 009/100 VUs, 30 complete and 0 interrupted iterations
default   [   2% ] 009/100 VUs  0m11.0s/9m00.0s

running (0m12.0s), 010/100 VUs, 30 complete and 0 interrupted iterations
default   [   2% ] 010/100 VUs  0m12.0s/9m00.0s

running (0m13.0s), 011/100 VUs, 30 complete and 0 interrupted iterations
default   [   2% ] 011/100 VUs  0m13.0s/9m00.0s

running (0m14.0s), 012/100 VUs, 30 complete and 0 interrupted iterations
default   [   3% ] 012/100 VUs  0m14.0s/9m00.0s

running (0m15.0s), 013/100 VUs, 30 complete and 0 interrupted iterations
default   [   3% ] 013/100 VUs  0m15.0s/9m00.0s

running (0m16.0s), 014/100 VUs, 31 complete and 0 interrupted iterations
default   [   3% ] 014/100 VUs  0m16.0s/9m00.0s

running (0m17.0s), 014/100 VUs, 31 complete and 0 interrupted iterations
default   [   3% ] 014/100 VUs  0m17.0s/9m00.0s

running (0m18.0s), 015/100 VUs, 31 complete and 0 interrupted iterations
default   [   3% ] 015/100 VUs  0m18.0s/9m00.0s

running (0m19.0s), 016/100 VUs, 31 complete and 0 interrupted iterations
default   [   4% ] 016/100 VUs  0m19.0s/9m00.0s

running (0m20.0s), 017/100 VUs, 31 complete and 0 interrupted iterations
default   [   4% ] 017/100 VUs  0m20.0s/9m00.0s

running (0m21.0s), 018/100 VUs, 31 complete and 0 interrupted itera
... [Output Truncated for Brevity] ...
Error: None

--- Performance Bottleneck Analysis ---
Based on the provided performance metrics from the load test, here is an analysis of the system's performance, potential bottlenecks, and suggestions for optimization:

### Analysis of Performance Metrics:

1. **Test Configuration:**
   - The test was configured to run with up to 100 Virtual Users (VUs) for a duration of 9 minutes, with a ramp-up and ramp-down period of 30 seconds each.

2. **Execution Summary:**
   - The test failed, indicating that the system did not handle the load as expected.
   - The output shows that the number of completed iterations per second is very low, especially considering the number of VUs.

3. **Iteration Completion:**
   - Initially, the number of completed iterations increases, but after a short period (around 10-12 seconds), the number of completed iterations stagnates significantly.
   - This suggests that the system is unable to handle the increasing load, leading to a bottleneck.

4. **Virtual User Utilization:**
   - The number of active VUs increases steadily, but the number of completed iterations does not scale proportionally.
   - This indicates that the system is not effectively utilizing the available VUs, likely due to a bottleneck that prevents further progress.

### Potential Bottlenecks and Scalability Issues:

1. **Resource Saturation:**
   - The system might be experiencing resource saturation, such as CPU, memory, or I/O, which prevents it from handling more requests efficiently.

2. **Database or Backend Service Bottleneck:**
   - If the application relies on a database or external services, these could be bottlenecks. Slow queries, connection limits, or high latency could be causing the system to slow down.

3. **Network Latency:**
   - High network latency or bandwidth limitations could be affecting the system's ability to process requests quickly.

4. **Application Logic:**
   - Inefficient application logic, such as synchronous processing or blocking operations, could be limiting the throughput.

### Suggestions for Optimization:

1. **Resource Monitoring:**
   - Monitor system resources (CPU, memory, disk I/O, network) during the test to identify any saturation points.
   - Use tools like Grafana, Prometheus, or similar to visualize and analyze resource usage.

2. **Database Optimization:**
   - Analyze database performance, optimize slow queries, and ensure indexes are used effectively.
   - Consider scaling the database or using caching mechanisms to reduce load.

3. **Application Profiling:**
   - Profile the application to identify any inefficient code paths or blocking operations.
   - Consider refactoring code to improve concurrency and reduce blocking.

4. **Load Balancing:**
   - Implement or optimize load balancing to distribute the load more evenly across servers or instances.

5. **Network Improvements:**
   - Optimize network configurations to reduce latency and improve throughput.
   - Consider using a Content Delivery Network (CDN) if applicable.

6. **Scalability Testing:**
   - Conduct further testing to identify the exact point of failure and test with different configurations to find optimal settings.

By addressing these potential bottlenecks and implementing the suggested optimizations, the system's performance under load can be improved, leading to better scalability and reliability.