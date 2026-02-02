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