from random import randint, choice


def generate_id():
    id = []

    alphabet = [chr(e) for e in range(65, 91)]
    alphabet.extend([chr(e) for e in range(97, 123)])

    for i in range(16):
        id.append(choice(alphabet))

    nums_count = randint(0, 15)

    for i in range(nums_count):
        what_replace = randint(-1, 13)
        del id[what_replace]
        id.insert(what_replace - 1, str(randint(0, 9)))

    return ''.join(id)


def coder(password):
    res = ''

    first_step = []
    for e in range(len(password)):
        first_step.extend([str(ord(password[e]))])
    first_step = ''.join(first_step)

    for e in range(len(first_step)):
        if int(first_step[e]) <= 4:
            alphabet = [chr(e) for e in range(65, 91 - 18)]
            alphabet.extend([chr(e) for e in range(97, 123 - 18)])
            res += alphabet[e]

        elif int(first_step[e]) <= 7:
            alphabet = [chr(e) for e in range(9 + 65, 91 - 9)]
            alphabet.extend([chr(e) for e in range(9 + 97, 123 - 9)])
            res += alphabet[e]

        elif int(first_step[e]) <= 9:
            alphabet = [chr(e) for e in range(18 + 65, 91)]
            alphabet.extend([chr(e) for e in range(18 + 97, 123)])
            res += alphabet[e]

    return res