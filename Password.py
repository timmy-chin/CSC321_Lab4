import bcrypt
from nltk.corpus import words

# Password to hash
password = b"super_secret_password"

# Generate salt and hash the password
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password, b"$2b$08$.YvniOnWyuv3.OHGUxogJu")

print(f"Salt: {salt}")
print(f"Hashed password: {hashed_password}")
words.words()