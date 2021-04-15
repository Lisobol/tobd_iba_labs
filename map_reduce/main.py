import random
import string
import os
from itertools import islice
import multiprocessing
import collections
from memory_profiler import profile



def gen_str(file_size_gb, filename='/home/lisobole/work/lab1.txt'):
    while os.path.getsize(filename) / (1024 * 1024 * 1024) < file_size_gb:
        print('Размер файла [Гб]:', os.path.getsize(filename) / (1024 * 1024 * 1024))
        strs = ''.join(
            [''.join(random.choice(string.ascii_letters) for i in range(random.randint(32, 62))) + '\n' for _ in
             range(0, 10000)])
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(strs)


def read_file(file_part):
    filename = '/home/lisobole/work/lab1.txt'
    arr = []
    with open(filename) as lines:
        count = sum(1 for _ in lines)
    third = int(count / 3)
    starts_ends = {1: [0, third - 1],
                   2: [third, third * 2 - 1],
                   3: [third * 2, count - 1]}
    with open(filename) as lines:
        for line in islice(lines, starts_ends.get(file_part)[0], starts_ends.get(file_part)[1]):
            arr.append(line)
    return arr


def mapper(num):
    res = read_file(num)
    counter = collections.Counter(res)
    return counter


def reduce(counters):
    counter = counters[0] + counters[1] + counters[2]
    return dict(sorted(counter.items(), key=lambda i: i[1], reverse=True))


@profile
def run_all():
    gen_str(1)
    pool = multiprocessing.Pool(3)

    mapped = pool.map(mapper, [1, 2, 3])
    reduced = reduce(mapped)
    print('Результат: ', list(reduced.items())[:100])


if __name__ == '__main__':
    run_all()
