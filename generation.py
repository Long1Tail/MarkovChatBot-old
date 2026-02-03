import random


def parse(text: str, dictionary_1: dict, dictionary_2: dict):
    text.replace('\n', ' ')
    for i in ',./?<>"\':;][}{=+-_)(*&^%$#@!№1234567890« ':
        text = text.replace(i, '')
    while text.count('  '):
        text = text.replace('  ', ' ')
    text = text.lower()
    text = text.split()
    for i in range(len(text) - 2):
        pare = [text[i], text[i + 1]]
        if ' '.join(pare) not in dictionary_1.keys():
            dictionary_1[' '.join(pare)] = []
        dictionary_1[' '.join(pare)].append(text[i + 2])
    for i in range(len(text) - 1):
        if text[i] not in dictionary_2.keys():
            dictionary_2[text[i]] = []
        dictionary_2[text[i]].append(text[i + 1])


def read_from_file(file):
    with open(file, 'r') as text:
        data = text.read()
        return data


def generate_pare(d1):
    k = random.choice(list(d1.keys()))
    return k + ' ' + random.choice(d1[k])


def generate(n: int, d1: dict, d2: dict):
    if n == 1:
        return random.choice(list(d2.keys()))
    elif n == 2:
        return generate_pare(d2)
    else:
        s = generate_pare(d2)
        while s not in d1.keys():
            s = generate_pare(d2)
        n -= 2
        s = s.split()
        while n:
            s.append(random.choice(d1[' '.join(s[-2:])]))
            n -= 1

    return ' '.join(s)

#
# d1 = {}
# d2 = {}
# parse(read_from_file('проба.txt'), d1, d2)
# print(generate(20, d1, d2))
