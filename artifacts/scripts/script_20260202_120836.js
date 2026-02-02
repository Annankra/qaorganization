import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Define performance thresholds
const responseTimeThreshold = 500; // 500ms
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
        http_req_duration: [`p(95)<${responseTimeThreshold}`], // 95% of requests must complete below 500ms
        errors: [`rate<${errorRateThreshold}`], // Error rate must be below 1%
    },
};

export default function () {
    const res = http.get('https://your-api-endpoint.com/mission');

    // Check if the response status is 200
    const checkRes = check(res, {
        'status is 200': (r) => r.status === 200,
    });

    // Record error if the check fails
    if (!checkRes) {
        errorRate.add(1);
    }

    // Simulate user think time
    sleep(1);
}