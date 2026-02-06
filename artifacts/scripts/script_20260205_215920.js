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

export default function () {
    let url = 'https://example.com/api/user/profile';
    let payload = JSON.stringify({
        username: 'testuser',
        email: 'testuser@example.com',
        password: 'newpassword123',
    });

    let params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    let res = http.put(url, payload, params);

    let success = check(res, {
        'is status 200': (r) => r.status === 200,
        'response time < 500ms': (r) => r.timings.duration < 500,
    });

    errorRate.add(!success);

    sleep(1);
}