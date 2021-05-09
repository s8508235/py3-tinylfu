import tinylfu
import time
import random
import functools
import logging

# long tail, assume [data_high_freq_start, data_high_freq_end] will take 80%,
# [data_high_freq_end, data_size] will take 20%
data_size = 10000
data = [i for i in range(data_size)]
test_times = data_size * 10
# sleep_duration = 0.00001
cache_size = int(data_size * 0.01)
data_high_freq_start = 0
data_high_freq_end = data_size * 0.2 - 1

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

logging.info(f'cache_size {cache_size}')


def tinylfu_speed():
    @tinylfu.TinyLFUCache(cache_size=cache_size)
    def my_getter(key: int):
        # time.sleep(sleep_duration)
        return data[key]

    now = int(time.time() * 1000)
    random.seed(now)
    for _ in range(test_times):
        r = random.randint(0, 4)
        if r == 0:
            key = random.randint(data_high_freq_start, data_high_freq_end)
        else:
            key = random.randint(data_high_freq_end + 1, data_size - 1)
        my_getter(key)

    logging.info(f'cache info {my_getter.cache_info()}')
    return int(time.time() * 1000) - now


def lru_speed():
    @functools.lru_cache(maxsize=cache_size)
    def my_getter(key: int):
        # time.sleep(sleep_duration)
        return data[key]

    now = int(time.time() * 1000)
    random.seed(now)
    for _ in range(test_times):
        r = random.randint(0, 4)
        if r == 0:
            key = random.randint(data_high_freq_start, data_high_freq_end)
        else:
            key = random.randint(data_high_freq_end + 1, data_size - 1)
        my_getter(key)

    logging.info(f'cache info {my_getter.cache_info()}')
    return int(time.time() * 1000) - now


def no_cache_speed():
    def my_getter(key: int):
        # time.sleep(sleep_duration)
        return data[key]

    now = int(time.time() * 1000)
    random.seed(now)
    for _ in range(test_times):
        r = random.randint(0, 4)
        if r == 0:
            key = random.randint(data_high_freq_start, data_high_freq_end)
        else:
            key = random.randint(data_high_freq_end + 1, data_size - 1)
        my_getter(key)
    return int(time.time() * 1000) - now


def main():
    logging.info(f"lru speed {lru_speed()} millsecs")
    logging.info(f"normal speed {no_cache_speed()} millsecs")
    logging.info(f"tinylfu speed {tinylfu_speed()} millsecs")


if __name__ == '__main__':
    main()