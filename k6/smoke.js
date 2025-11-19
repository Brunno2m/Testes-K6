import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 5,
  duration: '20s',
};

export default function () {
  http.get('http://127.0.0.1:5000/sum?a=1&b=2');
  sleep(1);
}
