import bcrypt
import secrets

def hash_password(password, salt):
    """Hashes the password with bcrypt algorithm and salt."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def generate_salt():
    """Generates a random salt."""
    return bcrypt.gensalt()

def main():
    passwords = ['Super']
    salt = generate_salt()

    print("Password\tSalt\t\tHashed Password")
    print("---------------------------------------------")
    for password in passwords:
        hashed_password = hash_password(password, salt)
        print(f"{password}\t\t{salt}\t{hashed_password}")

if __name__ == "__main__":
    main()
