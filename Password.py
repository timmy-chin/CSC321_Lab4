import sys

import bcrypt
from nltk.corpus import words
from datetime import datetime


def get_hashes():
    hashes = []
    with open("shadow.txt") as file:
        for hashed in file:
            hashed = hashed.replace("\n", "")
            hash_split = hashed.split(":")
            name = hash_split[0]
            hash_value = hash_split[1].encode("utf-8")
            salt = hash_value[0:29]
            hashes.append((name, salt, hash_value))
    return hashes


def crack_hash(num, start_index=0):
    start = datetime.now()
    count = 0
    name, salt, hash_value = user_hashes[num]
    for i in range(start_index, len(passwords)):
        password = passwords[i]
        hashed_code = bcrypt.hashpw(password.encode("utf-8"), salt)
        if hashed_code == hash_value:
            print(f"FOUND IT! Password for {name}: {password}")
            end = datetime.now()
            time_diff = end - start
            time_diff = time_diff.total_seconds()
            with open(f"password{num}.txt", "w") as file:
                file.write(
                    f"User: {name}\nPassword: {password}\nAttempts: {count}\nTotal Time: {time_diff}s\nSalt: {salt}\nHash: {hash_value}")
            return
        count += 1

        # Logging
        if count % 500 == 0:
            mid = datetime.now()
            mid_diff = mid - start
            mid_diff = mid_diff.total_seconds()
            print(f"Attempted: {count}, Last Word: {password}, Running time: {mid_diff}s")




if __name__ == "__main__":
    num = int(sys.argv[1])
    passwords = [password for password in words.words() if 6 <= len(password) <= 10]
    user_hashes = get_hashes()
    crack_hash(num)
