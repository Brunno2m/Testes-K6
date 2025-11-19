import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m', target: 100 },
    { duration: '30s', target: 200 },
    { duration: '30s', target: 0 },
  ],
};

export default function () {
  http.get('http://127.0.0.1:5000/sum?a=1&b=2');
  sleep(1);
}
