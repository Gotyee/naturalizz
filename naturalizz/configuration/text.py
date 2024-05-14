# Import Required Module
# Empty password list
import itertools

import pikepdf
from tqdm import tqdm


def generate_combinations():
    # Define the characters and digits to be used
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    combinations = []
    # Generate combinations of length 1 to 20
    for length in tqdm(range(1, 21), desc="Generating combinations", unit="length"):
        with tqdm(
            total=int(pow(len(characters), length)),
            desc=f"Length {length}",
            unit="combination",
        ) as pbar:
            # Generate all possible combinations
            for combination in itertools.product(characters, repeat=length):
                combinations.append("".join(combination))
                pbar.update(1)
    return combinations


# Generate list of combinations
passwords = generate_combinations()

# iterate over passwords
for password in tqdm(passwords, "Cracking PDF File"):
    try:
        # open PDF file and check each password
        with pikepdf.open(
            "/Users/reddariel/Downloads/B2405070059.pdf", password=password
        ) as p:
            # If password is correct, break the loop
            print("[+] Password found:", password)
            break

    # If password will not match, it will raise PasswordError
    except pikepdf._qpdf.PasswordError:
        # if password is wrong, continue the loop
        continue
