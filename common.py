from random import seed as randseed, choice

OCR_N_WORDS = 2
with open("wordpool.txt", "r") as f:
    WORDPOOL = [l.strip() for l in f.readlines()]

def get_random_text(seed: int | None = None) -> str:
    # Hash team name and get a corresponding string (2 words)
    if seed:
        randseed(hash(seed))
    text_to_gen = ""
    #  (14 <= len(text_to_gen) <= 16):
    while len(text_to_gen) != 16:
        text_to_gen = ' '.join([choice(WORDPOOL) for _ in range(OCR_N_WORDS)])

    return text_to_gen

def green(message):
    return '\033[92m' + message + '\033[0m'

def red(message):
    return '\033[91m' + message + '\033[0m'

def print_divider(): print('#'*25)