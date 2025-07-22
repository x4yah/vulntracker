import string
from random import choice

LETTERTS = [
    # letras
    "alpha",
    "omega",
    "delta",
    "foxtrot",
    "theta",
    "bravo",
    "django",
    "rusty",
    "cargo",
    "charlie",
    "tango",
    "romeo",
    "zulu",
    "yankee",
    "juliette",
]

ATTRIBUTES = [
    # starts
    "nova",
    # gods
    "ares",
    "hades",
    "poseidon",
    "zeus",
    "sheldon",
    "penny",
    "barney",
    "ted",
    "robin",
    "max",
    "onyx",
    "acura",
    "falcon",
    "dotexe",
    "destroyed",
    "rum",
    "whiskey",
    "elder",
    "arcane",
]


def generate_code_name(capitalize=False, uppercase=False, separator="—"):
    words = [choice(LETTERTS), choice(ATTRIBUTES)]
    if capitalize:
        words = list(map(str.capitalize, words))
    if uppercase:
        words = list(map(str.upper, words))
    return separator.join(words)
