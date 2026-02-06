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