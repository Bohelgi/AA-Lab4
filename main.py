import random

def H_poly(input_str):
    bytes_representation = input_str.encode('utf-8')

    if len(bytes_representation) % 2 != 0:
        bytes_representation += b'\x00'

    result = []
    for i in range(0, len(bytes_representation), 2):
        value = (bytes_representation[i] << 8) + bytes_representation[i + 1]
        result.append(value)

    return result


class BloomFilter:
    def __init__(self, s):
        self.s = s
        self.N = 2**16
        self.filter_array = [0] * self.N
        self.hash_functions = [self.generate_random_hash() for _ in range(s)]

    def generate_random_hash(self):
        return random.randint(1, 2**30)

    def add_element(self, element):
        hashed_values = [hash_val % self.N for hash_val in H_poly(element)[:self.s]]
        for val in hashed_values:
            self.filter_array[val] = 1

    def check_element(self, element):
        hashed_values = [hash_val % self.N for hash_val in H_poly(element)[:self.s]]
        return all(self.filter_array[val] == 1 for val in hashed_values)

    def clear_filter(self):
        self.filter_array = [0] * self.N


bloom_filter = BloomFilter(s=3)

bloom_filter.add_element("message1")

result = bloom_filter.check_element("message1")
print(result)


bloom_filter.clear_filter()


def bloom_filter_experiment(n, a_values, s):
    results = []

    for a in a_values:
        p_err_avg = bloom_filter_experiment_single(n, a, s)
        results.append((a, p_err_avg))

    return results


def bloom_filter_experiment_single(n, a, s):
    N = 2**16
    M = 100
    p_err_total = 0

    for _ in range(M):
        bloom_filter = BloomFilter(s=s)

        random_messages = [str(random.getrandbits(32)) for _ in range(int(a * N))]
        for message in random_messages:
            bloom_filter.add_element(message)

        false_positive_count = 0
        for _ in range(N):
            test_message = str(random.getrandbits(32))
            if bloom_filter.check_element(test_message):
                false_positive_count += 1

        p_err = false_positive_count / N
        p_err_total += p_err

    p_err_avg = p_err_total / M
    return p_err_avg

a_values = [0.05, 0.1, 0.15, 0.20, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
s = 3

results = bloom_filter_experiment(100, a_values, s)

for a, p_err_avg in results:
    print(f"Estimated Error Probability for a={a}: {p_err_avg}")