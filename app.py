import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<numberString>')
def isPrime(numberString):
    number = int(numberString)
    if number > 1:
        for i in range(2, number//2 + 1):
            if (number % i) == 0:
                return (numberString + ' is not prime')
        else:
            return (numberString + ' is prime')
    else:
        return (numberString + ' is not prime')
    #primeness algorithm adapted from https://www.geeksforgeeks.org/python-program-to-check-whether-a-number-is-prime-or-not/
    
@app.route('/primesStored')
def primesStored():
    return 'The following prime numbers are stored...'

    
