from lookup_tables import *


def sixteen_keys(key):
    key = ''.join(key[p56[i] - 1] for i in range(56))
    keys = []
    left_key, right_key = key[:28], key[28:]
    for i in range(16):
        left_key = left_key[shift_value[i]:] + left_key[:shift_value[i]]
        right_key = right_key[shift_value[i]:] + right_key[:shift_value[i]]
        keys.append(left_key + right_key)
    keys = [''.join(k[p48[i] - 1] for i in range(48)) for k in keys]
    return keys


def foo(r, key):
    r = ''.join(r[e48[i] - 1] for i in range(48))
    bar = int(key, 2) ^ int(r, 2)
    bar = '{:048b}'.format(bar)
    bar = [(bar[i:i + 6]) for i in range(0, 48, 6)]
    baz = []
    for k, b in enumerate(bar):
        i = int((b[0] + b[5]), 2)
        j = int(b[1:5], 2)
        baz.append('{:04b}'.format(sBox[k][i * 16 + j]))
    baz = ''.join(b for b in baz)
    baz = ''.join(baz[pf32[i] - 1] for i in range(32))
    return baz


def encrypt(text, keys):
    # assumes that text is 64 bit
    text = ''.join(text[ip64[i] - 1] for i in range(64))
    left, right = text[:32], text[32:]
    for i in range(16):
        old_left = left
        left = right
        right = int(old_left, 2) ^ int(foo(right, keys[i]), 2)
        right = '{:032b}'.format(right)
    cipher = right + left
    cipher = ''.join(cipher[fp64[i] - 1] for i in range(64))
    return cipher
