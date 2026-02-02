import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Define thresholds
const responseTimeThreshold = 200; // in milliseconds
const errorRateThreshold = 0.01; // 1% error rate

// Custom metrics
let errorRate = new Rate('errors');

export let options = {
    stages: [
        { duration: '1m', target: 50 }, // Ramp-up to 50 users over 1 minute
        { duration: '3m', target: 50 }, // Stay at 50 users for 3 minutes
        { duration: '1m', target: 0 },  // Ramp-down to 0 users over 1 minute
    ],
    thresholds: {
        http_req_duration: [`p(95)<${responseTimeThreshold}`], // 95% of requests must complete below 200ms
        errors: [`rate<${errorRateThreshold}`], // Error rate must be below 1%
    },
};

export default function () {
    const url = 'https://example.com/login'; // Replace with the actual login URL
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

    // Check if the response status is 200
    const success = check(res, {
        'is status 200': (r) => r.status === 200,
    });

    // Record error rate
    errorRate.add(!success);

    // Simulate user think time
    sleep(1);
}