### Description
An in memory cache policy.

Its core is an admission policy tiny-lfu which is composed of CountMinSketch and BloomFilter.

CountMinSketch is to get the approximate count and BloomFilter decide to check or not.

Derive from [here](https://github.com/dgryski/go-tinylfu)

### Goal
- Remove/Aging improvement
- concurrently safe
- profiling
- better unit test
- load test

### Further reading
- http://highscalability.com/blog/2016/1/25/design-of-a-modern-cache.html
- https://github.com/ben-manes/caffeine/wiki