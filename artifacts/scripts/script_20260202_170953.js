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