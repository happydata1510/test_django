from django.core.management.utils import get_random_secret_key

def generate_secret_key():
    secret_key = get_random_secret_key()
    print(secret_key)

if __name__ == "__main__":
    generate_secret_key()