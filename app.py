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
        i = 2;
        while i*i <=number:
            if number % i == 0:
                return (numberString + ' is not prime')
            i += 1
        addPrime(number)
        return (numberString + ' is prime') 
        #for i in range(2, number//2 + 1):
         #   if (number % i) == 0:
          #      return (numberString + ' is not prime')
        #else:
            #Add the number to the list
         #   addPrime(number)
          #  return (numberString + ' is prime')
    else:
        return (numberString + ' is not prime')
    #primeness algorithm adapted from https://www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
    
@app.route('/primesStored')
def primesStored():
    ls = [];
    val = 0;
    for i in range (0, cache.llen(primes)):
        val = cache.lpop(primes)
        cache.rpush(primes, val)
        if val not in ls: #Only add items to the retun list if they arent already in it (no duplicates)
            ls.extend([val])
        i += 1

    return str(ls)

@app.route('/clearPrimesStored')
def clearPrimesStored():
    for i in range (0, cache.llen(primes)):
        cache.lpop(primes)
    return "List of primesStore has been cleared..."


    
