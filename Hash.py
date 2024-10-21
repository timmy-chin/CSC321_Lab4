from Crypto.Hash import SHA256
from datetime import datetime


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


def get_partner_bytes(key, bits):
    mask = 0b0001
    lst = []
    count = 0
    while count < bits:
        byte = key ^ mask  # 0b0001
        print(f"key: {bin(key)[2:]}")
        str = bits_to_string(byte)
        lst.append(str)
        mask = mask << 1
        count += 1
    return lst


def bits_to_string(binary_literal, encoding='latin-1'):
    bit_string = bin(binary_literal)[2:]
    print(bit_string)
    if len(bit_string) % 8 != 0:
        bit_string = bit_string.zfill(len(bit_string) + (8 - len(bit_string) % 8))
    byte_array = bytearray(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))
    return byte_array.decode(encoding)


def bits_str_to_string(bit_string, encoding='latin-1'):
    if len(bit_string) % 8 != 0:
        bit_string = bit_string.zfill(len(bit_string) + (8 - len(bit_string) % 8))
    byte_array = bytearray(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))
    return byte_array.decode(encoding)


def find_str_collisions(bits):
    count = 0
    key = 0b0

    while count < 2 ** bits:
        lst = []
        str_key = bits_to_string(key)
        lst = get_partner_bytes(key, bits)
        for char in lst:
            m0 = str_key
            m1 = char
            print(f"Trying: {m0}, {m1}")
            if check_collisions(m0, m1, bits):
                return (m0, m1)
        key += 1
        count += 1


def find_collisions(bits):
    map = create_str_pairs(bits)
    lst = []
    for key, values in map.items():
        m0 = key
        for val in values:
            m1 = val
            print(f"Trying: {m0},{m1}")
            if check_collisions(m0, m1, bits):
                lst.append((m0, m1))
    return lst


def check_collisions(m0, m1, bits, case_count):
    h1 = sha256_hash(m0, bits)
    h2 = sha256_hash(m1, bits)
    print(
        f"m0,m1: {(m0, m1)}, h1: {h1}, h2: {h2}, Hamming Distance: {hamming_distance_bytes(m0, m1)}, case: {case_count}")

    return h1 == h2


import random


def generate_random_binary_string(length):
    return ''.join(random.choice('01') for _ in range(length))


def flip_random_bit(binary_string):
    binary_list = list(binary_string)

    flip_index = random.randint(0, len(binary_list) - 1)

    binary_list[flip_index] = '1' if binary_list[flip_index] == '0' else '0'

    return ''.join(binary_list)


def new_and_improved_find_collision(bits):
    choices = [8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88]
    case_count = 0
    start = datetime.now()
    while True:
        index = random.randint(0, 10)
        base_string = generate_random_binary_string(choices[index])
        new_string = flip_random_bit(base_string)
        print(f"\nm0 bin: {base_string}")
        print(f"m1 bin: {new_string}")
        m0 = bits_str_to_string(base_string)
        m1 = bits_str_to_string(new_string)
        if check_collisions(m0, m1, bits, case_count):
            end = datetime.now()
            time_diff = end - start
            return (m0, m1, time_diff, case_count)
        case_count += 1


def get_all_cases():
    bits = 8
    file = open("result.txt", "a")
    while bits < 51:
        m0, m1, time, input_size = new_and_improved_find_collision(bits)
        file.write(f"B i t s: {bits}\nm0: {m0}\nm1: {m1}\nTime: {time}\nInput_size: {input_size}\n\n\n")
        bits += 2


if __name__ == "__main__":
    # str1 = "a"
    # str2= "b"
    # print(hamming_distance_bytes(str1, str2))
    # print(find_collisions(25))
    # Example usage
    # base_string = generate_random_binary_string(36)
    # new_string = flip_random_bit(base_string)
    # print(base_string)
    # print(new_string)
    # print(bits_str_to_string(base_string))
    # print(bits_str_to_string(new_string))
    # print(new_and_improved_find_collision(16))
    get_all_cases()


