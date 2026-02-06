--- Performance Load Test Plan ---
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export let errorRate = new Rate('errors');

export let options = {
    stages: [
        { duration: '1m', target: 10 }, // ramp up to 10 users
        { duration: '3m', target: 10 }, // stay at 10 users
        { duration: '1m', target: 0 },  // ramp down to 0 users
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
        errors: ['rate<0.01'], // error rate must be less than 1%
    },
};

const BASE_URL = 'https://your-application-url.com';
const USERNAME = 'testuser';
const PASSWORD = 'testpassword';

export default function () {
    // User login
    let loginRes = http.post(`${BASE_URL}/api/login`, {
        username: USERNAME,
        password: PASSWORD,
    });

    check(loginRes, {
        'logged in successfully': (resp) => resp.status === 200,
    }) || errorRate.add(1);

    let authToken = loginRes.json('token');

    // Update user profile settings
    let profileRes = http.put(`${BASE_URL}/api/user/profile`, JSON.stringify({
        email: 'newemail@example.com',
        name: 'New Name',
    }), {
        headers: {
            Authorization: `Bearer ${authToken}`,
            'Content-Type': 'application/json',
        },
    });

    check(profileRes, {
        'profile updated successfully': (resp) => resp.status === 200,
    }) || errorRate.add(1);

    // Upload profile image
    let imageUploadRes = http.post(`${BASE_URL}/api/user/profile/image`, {
        file: http.file(open('./path/to/image.jpg', 'b'), 'image.jpg'),
    }, {
        headers: {
            Authorization: `Bearer ${authToken}`,
        },
    });

    check(imageUploadRes, {
        'image uploaded successfully': (resp) => resp.status === 200,
    }) || errorRate.add(1);

    // Email verification
    let emailVerifyRes = http.get(`${BASE_URL}/api/user/verify-email`, {
        headers: {
            Authorization: `Bearer ${authToken}`,
        },
    });

    check(emailVerifyRes, {
        'email verified successfully': (resp) => resp.status === 200,
    }) || errorRate.add(1);

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
        script: /var/folders/05/0z812bxj2lz4n79z43jkk1y00000gp/T/tmpnbbiquc2.js
        output: -

     scenarios: (100.00%) 1 scenario, 10 max VUs, 5m30s max duration (incl. graceful stop):
              * default: Up to 10 looping VUs for 5m0s over 3 stages (gracefulRampDown: 30s, gracefulStop: 30s)


running (0m01.0s), 01/10 VUs, 717 complete and 0 interrupted iterations
default   [   0% ] 01/10 VUs  0m01.0s/5m00.0s

running (0m02.0s), 01/10 VUs, 1491 complete and 0 interrupted iterations
default   [   1% ] 01/10 VUs  0m02.0s/5m00.0s

running (0m03.0s), 01/10 VUs, 2234 complete and 0 interrupted iterations
default   [   1% ] 01/10 VUs  0m03.0s/5m00.0s

running (0m04.0s), 01/10 VUs, 2981 complete and 0 interrupted iterations
default   [   1% ] 01/10 VUs  0m04.0s/5m00.0s

running (0m05.0s), 01/10 VUs, 3729 complete and 0 interrupted iterations
default   [   2% ] 01/10 VUs  0m05.0s/5m00.0s

running (0m06.0s), 01/10 VUs, 4498 complete and 0 interrupted iterations
default   [   2% ] 01/10 VUs  0m06.0s/5m00.0s

running (0m07.0s), 02/10 VUs, 5512 complete and 0 interrupted iterations
default   [   2% ] 02/10 VUs  0m07.0s/5m00.0s

running (0m08.0s), 02/10 VUs, 6980 complete and 0 interrupted iterations
default   [   3% ] 02/10 VUs  0m08.0s/5m00.0s

running (0m09.0s), 02/10 VUs, 8421 complete and 0 interrupted iterations
default   [   3% ] 02/10 VUs  0m09.0s/5m00.0s

running (0m10.0s), 02/10 VUs, 9953 complete and 0 interrupted iterations
default   [   3% ] 02/10 VUs  0m10.0s/5m00.0s

running (0m11.0s), 02/10 VUs, 11469 complete and 0 interrupted iterations
default   [   4% ] 02/10 VUs  0m11.0s/5m00.0s

running (0m12.0s), 02/10 VUs, 12979 complete and 0 interrupted iterations
default   [   4% ] 02/10 VUs  0m12.0s/5m00.0s

running (0m13.0s), 02/10 VUs, 14449 complete and 0 interrupted iterations
default   [   4% ] 02/10 VUs  0m13.0s/5m00.0s

running (0m14.0s), 03/10 VUs, 16411 complete and 0 interrupted iterations
default   [   5% ] 03/10 VUs  0m14.0s/5m00.0s

running (0m15.0s), 03/10 VUs, 18652 complete and 0 interrupted iterations
default   [   5% ] 03/10 VUs  0m15.0s/5m00.0s

running (0m16.0s), 03/10 VUs, 20837 complete and 0 interrupted iterations
default   [   5% ] 03/10 VUs  0m16.0s/5m00.0s

running (0m17.0s), 03/10 VUs, 23045 complete and 0 interrupted iterations
default   [   6% ] 03/10 VUs  0m17.0s/5m00.0s

running (0m18.0s), 03/10 VUs, 25303 complete and 0 interrupted iterations
default   [   6% ] 03/10 VUs  0m18.0s/5m00.0s

running (0m19.0s), 03/10 VUs, 27466 complete and 0 interrupted iterations
default   [   6% ] 03/10 VUs  0m19.0s/5m00.0s

running (0m20.0s), 03/10 VUs, 29724 complete and 0 interrupted iterations
default   [   7% ] 03/10 VUs  0m20.0s/5m00.0s

running (0m21.0s), 04/10 VUs, 32649 complete and 0 interrupted iterations
default   [   7% ] 0
... [Output Truncated for Brevity] ...
Error: None

--- Performance Bottleneck Analysis ---
Based on the provided performance metrics from the load test, here is an analysis of the system's performance, potential bottlenecks, scalability issues, and suggestions for optimization:

### Analysis

1. **Test Configuration and Execution:**
   - The test was configured to run with a maximum of 10 Virtual Users (VUs) over a duration of 5 minutes with a 30-second graceful ramp-down and stop.
   - The test failed, indicating that the system did not meet the expected performance criteria.

2. **Performance Metrics:**
   - The test started with 1 VU and gradually increased to 4 VUs within the first 21 seconds.
   - The number of complete iterations increased rapidly, suggesting that the system could handle the initial load effectively.
   - However, the test failed early, which might indicate a potential bottleneck or a configuration issue.

3. **Potential Bottlenecks:**
   - **Resource Limitation:** The rapid increase in iterations suggests that the system might be initially capable of handling the load, but a resource limitation (CPU, memory, network bandwidth) could be causing the test to fail as more VUs are introduced.
   - **Concurrency Handling:** The system might have issues handling concurrent requests efficiently, leading to failures as the number of VUs increases.
   - **Configuration Limits:** There might be configuration limits (e.g., thread pool size, connection limits) that are being hit as the load increases.

4. **Scalability Issues:**
   - The system's ability to scale with increasing VUs is questionable since the test failed early. This suggests that the system might not be able to handle higher loads or scale effectively beyond a certain point.

5. **Regression Indicators:**
   - The test failure could indicate a regression if previous tests with similar configurations were successful. This might be due to recent changes in the system or its environment.

### Suggestions for Optimization

1. **Resource Monitoring:**
   - Monitor CPU, memory, disk I/O, and network usage during the test to identify resource bottlenecks.
   - Ensure that the system has adequate resources to handle the expected load.

2. **Concurrency and Configuration Tuning:**
   - Review and optimize server configurations related to concurrency, such as thread pools, database connections, and network settings.
   - Consider increasing limits if they are being reached prematurely.

3. **Load Balancing:**
   - Implement or optimize load balancing strategies to distribute the load more evenly across servers or instances.

4. **Code Optimization:**
   - Profile the application to identify inefficient code paths or queries that could be optimized for better performance under load.

5. **Incremental Load Testing:**
   - Conduct incremental load tests to gradually increase the load and identify the point at which performance degrades.
   - Use these tests to pinpoint specific areas that need optimization.

6. **Review Recent Changes:**
   - If this test result is a regression, review recent changes to the application or infrastructure that could have impacted performance.

By addressing these areas, you can improve the system's ability to handle higher loads, reduce bottlenecks, and ensure scalability.