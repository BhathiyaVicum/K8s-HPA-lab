import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 5 },
    { duration: '1m',  target: 30 },
    { duration: '3m',  target: 60 },
    { duration: '1m',  target: 10 },
    { duration: '30s', target: 0 },
  ],
};

const BASE = __ENV.BASE_URL || 'http://flask-svc.hpa-lab.svc.cluster.local';

export default function () {
  const r = http.get(`${BASE}/work`);
  check(r, { 'status 200': (r) => r.status === 200 });
  sleep(0.1);
}