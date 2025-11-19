import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
    { duration: '20s', target: 5 },
    { duration: '10s', target: 200 },
    { duration: '20s', target: 5 },
  ],
};

export default function () {
  http.get('http://127.0.0.1:5000/sum?a=1&b=2');
  sleep(1);
}
