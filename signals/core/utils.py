import itertools
from functools import reduce

import numpy as np


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)


class MathUtils:
    @staticmethod
    def pgcd2(a, b):
        """pgcd(a,b): calcul du 'Plus Grand Commun Diviseur' entre les 2 nombres entiers a et b"""
        while b: a, b = b, a % b
        return a

    @classmethod
    def pgcd(cls, *n):
        """Calcul du 'Plus Grand Commun Diviseur' de n valeurs entières (Euclide)"""
        p = cls.pgcd2(n[0], n[1])
        for x in n[2:]:
            p = cls.pgcd2(p, x)
        return p

    @classmethod
    def ppcm2(cls, a, b):
        """ppcm(a,b): calcul du 'Plus Petit Commun Multiple' entre 2 nombres entiers a et b"""
        if (a == 0) or (b == 0):
            return 0
        else:
            return (a * b) // cls.pgcd2(a, b)

    @classmethod
    def ppcm(cls, *n):
        """Calcul du 'Plus Petit Commun Multiple' de n (>=2) valeurs entières (Euclide)"""

        if any(isinstance(k, float) for k in n):
            N = 10 ** max(len(k.split('.')[1]) if '.' in k else 0 for k in map(str, n))
            n = tuple(int(N * k) for k in n)
        else:
            N = 1

        p = abs(n[0] * n[1]) // cls.pgcd2(n[0], n[1])
        for x in n[2:]:
            p = abs(p * x) // cls.pgcd2(p, x)
        return p / N
