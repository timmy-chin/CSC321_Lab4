from Crypto.Hash import SHA256
from datetime import datetime
import random


def sha256_hash(input_string, bits):
    hasher = SHA256.new()
    hasher.update(input_string.encode())
    sha256_hash = hasher.digest()
    hash_int = int.from_bytes(sha256_hash, 'big')
    truncated_hash = hash_int & ((1 << bits) - 1)
    return truncated_hash


def hamming_distance_bytes(str1, str2):
    bytes1 = str1.encode('utf-8')
    bytes2 = str2.encode('utf-8')

    distance = 0
    for byte1, byte2 in zip(bytes1, bytes2):
        xor_result = byte1 ^ byte2
        distance += bin(xor_result).count('1')
    return distance


def bits_str_to_string(bit_string, encoding='latin-1'):
    if len(bit_string) % 8 != 0:
        bit_string = bit_string.zfill(len(bit_string) + (8 - len(bit_string) % 8))
    byte_array = bytearray(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))
    return byte_array.decode(encoding)


def generate_random_binary_string(length):
    return ''.join(random.choice('01') for _ in range(length))


def flip_random_bit(binary_string):
    binary_list = list(binary_string)
    flip_index = random.randint(0, len(binary_list) - 1)
    binary_list[flip_index] = '1' if binary_list[flip_index] == '0' else '0'
    return ''.join(binary_list)


def check_collisions(m0, m1, bits, case_count, hash_map):
    h1 = sha256_hash(m0, bits)
    h2 = sha256_hash(m1, bits)
    if h1 == h2:
        return m0, m1
    elif h1 in hash_map:
        return m0, hash_map[h1]
    elif h2 in hash_map:
        return m1, hash_map[h2]
    else:
        hash_map[h1] = m0
        hash_map[h2] = m1
        return None


def find_collisions(bits):
    case_count = 0
    start = datetime.now()
    hash_map = {}
    hash_set = set()
    while True:
        index = random.randint(1, 100)
        base_string = generate_random_binary_string(index)
        m0 = bits_str_to_string(base_string)
        if m0 in hash_set:
            continue
        new_string = flip_random_bit(base_string)
        m1 = bits_str_to_string(new_string)
        if m1 in hash_set:
            continue
        hash_set.add(m0)
        hash_set.add(m1)
        result = check_collisions(m0, m1, bits, case_count, hash_map)
        if result is not None:
            m0, m1 = result
            h0 = sha256_hash(m0, bits)
            h1 = sha256_hash(m1, bits)
            end = datetime.now()
            time_diff = end - start
            return m0, m1, time_diff, case_count, h0, h1
        case_count += 1
        print(f"Bits: {bits} Attempt: {case_count}")


def get_all_cases():
    bits = 8
    file = open("result.txt", "a")
    while bits < 51:
        m0, m1, time, input_size, h0, h1 = find_collisions(bits)
        file.write(f"B i t s: {bits}\nm0: {m0}\nm1: {m1}\nh0: {h0}\nh1: {h1}\nTime: {time}\nAttempts: {input_size}\n\n\n")
        bits += 2


if __name__ == "__main__":
    get_all_cases()

