import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '1m', target: 50 }, // Ramp-up to 50 virtual users over 1 minute
        { duration: '3m', target: 50 }, // Stay at 50 virtual users for 3 minutes
        { duration: '1m', target: 0 },  // Ramp-down to 0 virtual users over 1 minute
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
        http_req_failed: ['rate<0.01'],   // Error rate must be less than 1%
    },
};

export default function () {
    const res = http.get('https://your-api-endpoint.com/mission');
    
    check(res, {
        'status is 200': (r) => r.status === 200,
        'response time is below 500ms': (r) => r.timings.duration < 500,
    });

    sleep(1);
}