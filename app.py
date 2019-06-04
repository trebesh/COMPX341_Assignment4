import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)
primes = "NoSQLStored"


def addPrime(num):
    #Add the new prime value to the
    cache.rpush(primes, num)
    return ('Adding to primes list...')


#    retries = 5
#    while True:
#        try:
#            return cache.incr('hits')
#        except redis.exceptions.ConnectionError as exc:
#            if retries == 0:
#                raise exc
#            retries -= 1
#            time.sleep(0.5)


@app.route('/')
def hello():
    #count = get_hit_count()
    return 'Hello World!'# I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<numberString>')
def isPrime(numberString):
    number = int(numberString)
    if number > 1:
        for i in range(2, number//2 + 1):
            if (number % i) == 0:
                return (numberString + ' is not prime')
        else:
            #Add the number to the list
            addPrime(number)
            return (numberString + ' is prime')
    else:
        return (numberString + ' is not prime')
    #primeness algorithm adapted from https://www.geeksforgeeks.org/python-program-to-check-whether-a-number-is-prime-or-not/
    
@app.route('/primesStored')
def primesStored():
    #while (cache.llen(primes) != 0):
        #print(cache.lpop(primes))
    return str(cache.lrange(primes, 0, -1))

    
