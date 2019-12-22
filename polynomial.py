# polynomial.py

class Polynomial:

    def __init__(self, *coefficients):
        if isinstance(coefficients[0], list):
            self.polynomial = coefficients[0]
        elif isinstance(coefficients[0], dict):
            maximum = 0
            for i in coefficients[0]:
                maximum = max(i, maximum)
            a = [0 for i in range(maximum + 1)]
            for i in coefficients[0]:
                a[i] = coefficients[0][i]
            self.polynomial = a
        elif isinstance(coefficients[0], Polynomial):
            self.polynomial = coefficients[0].polynomial
        else:
            a = []
            for i in coefficients:
                a.append(i)
            self.polynomial = a

    def __repr__(self):
        return "Polynomial " + str(self.polynomial)

    def __str__(self):
        s = ""
        for i in range(len(self.polynomial) - 1, 0, -1):
            if self.polynomial[i] != 0:
                if i != len(self.polynomial) - 1:
                    s += " "
                    if self.polynomial[i] < 0:
                        s += '- '
                    else:
                        s += '+ '
                else:
                    if self.polynomial[i] < 0:
                        s += '-'
                if abs(self.polynomial[i]) != 1:
                    s += str(abs(self.polynomial[i]))
                if i != 1:
                    s += 'x^' + str(i)
                else:
                    s += 'x'
        if self.polynomial[0] != 0:
            if len(self.polynomial) != 1:
                if self.polynomial[0] < 0:
                    s += ' - '
                else:
                    s += ' + '
            else:
                if self.polynomial[0] < 0:
                    s += '-'
            s += str(abs(self.polynomial[0]))

        return s

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return other.polynomial == self.polynomial
        else:
            if len(self.polynomial) == 1:
                return self.polynomial[0] == other
            else:
                return False

    def __add__(self, other):
        if isinstance(other, Polynomial):
            a = [0 for i in range(max(len(self.polynomial), len(other.polynomial)))]
            for i in range(len(a)):
                if len(self.polynomial) > i:
                    a[i] += self.polynomial[i]
                if len(other.polynomial) > i:
                    a[i] += other.polynomial[i]
            self.polynomial = a
            i = len(self.polynomial) - 1
            while i > 0:
                if self.polynomial[i] == 0:
                    self.polynomial.pop()
                    i -= 1
                else:
                    break
            return self
        else:
            self.polynomial[0] += other
            return self

    __radd__ = __add__

    def __neg__(self):
        for i in range(len(self.polynomial)):
            self.polynomial[i] = -self.polynomial[i]
        return self

    def __sub__(self, other):
        if isinstance(other, Polynomial):
            a = [0 for i in range(max(len(self.polynomial), len(other.polynomial)))]
            for i in range(len(a)):
                if len(self.polynomial) > i:
                    a[i] += self.polynomial[i]
                if len(other.polynomial) > i:
                    a[i] -= other.polynomial[i]
            self.polynomial = a
            i = len(self.polynomial) - 1
            while i > 0:
                if self.polynomial[i] == 0:
                    self.polynomial.pop()
                    i -= 1
                else:
                    break
            return self
        else:
            self.polynomial[0] -= other
            return self

    def __rsub__(self, other):
        return -(self - other)

    def __call__(self, x):
        const = 1
        total = 0
        for i in range(len(self.polynomial)):
            total += self.polynomial[i] * const
            const *= x
        return total

    def degree(self):
        return len(self.polynomial) - 1

    def der(self, d=1):
        for i in range(d):
            a = []
            for i in range(1, len(self.polynomial)):
                a.append(self.polynomial[i] * i)
            self.polynomial = a
        return self

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            a = [0 for i in range(self.degree() + other.degree() + 1)]
            for i in range(len(self.polynomial)):
                for j in range(len(other.polynomial)):
                    a[i + j] += self.polynomial[i] * other.polynomial[j]
            self.polynomial = a
        else:
            for i in range(len(self.polynomial)):
                self.polynomial[i] *= other
        return self

    __rmul__ = __mul__

    def __mod__(self, other):
        if isinstance(other, Polynomial):
            while self.degree() >= other.degree():
                const = self.polynomial[-1] / other.polynomial[-1]
                for i in range(other.degree() + 1):
                    self.polynomial[-i - 1] -= const * other.polynomial[-i - 1]
                i = len(self.polynomial) - 1
                while i > 0:
                    if self.polynomial[i] == 0:
                        self.polynomial.pop()
                        i -= 1
                    else:
                        break
        else:
            self.polynomial[0] %= other
        return self

    def __rmod__(self, other):
        if isinstance(other, Polynomial):
            return other % self
        else:
            self.polynomial[0] = other % self.polynomial[0]
            return self

    def gcd(self, other):
        if isinstance(other, Polynomial):
            if other.polynomial == [0]:
                return self
            else:
                return other.gcd(self % other)
        else:
            if other == 0:
                return self
            else:
                return Polynomial(other).gcd((self % other).polynomial[0])

    def __iter__(self):
        self.a = 0
        return self

    def __next__(self):
        if self.a == len(self.polynomial):
            raise StopIteration
        b = (self.a, self.polynomial[self.a])
        self.a += 1
        return b



class RealPolynomial(Polynomial):
    def __init__(self, *coefficients):
        self.polynomial = Polynomial(*coefficients).polynomial

    def __call__(self, x):
        const = 1
        total = 0
        for i in range(len(self.polynomial)):
            total += self.polynomial[i] * const
            const *= x
        return total

    def find_root(self):
        a = -(10 ** 9)
        b = 10 ** 9
        eps = 10 ** (-7)
        if self.__call__(b) > 0:
            while b - a > eps:
                m = (b + a) / 2
                if self.__call__(m) >= 0:
                    b = m
                else:
                    a = m
        else:
            while b - a > eps:
                m = (b + a) / 2
                if self.__call__(m) <= 0:
                    b = m
                else:
                    a = m
        return b


class QuadraticPolynomial(Polynomial):
    def __init__(self, *coefficients):
        self.polynomial = Polynomial(*coefficients).polynomial


    def __call__(self, x):
        const = 1
        total = 0
        for i in range(len(self.polynomial)):
            total += self.polynomial[i] * const
            const *= x
        return total

    def solve(self):
        if len(self.polynomial) == 2:
            return [RealPolynomial(self.polynomial).find_root()]
        else:
            D = self.polynomial[1] ** 2 - 4 * self.polynomial[0] * self.polynomial[2]
            if abs(D) < 10 ** (-6):
                return [-self.polynomial[1] / (2 * self.polynomial[0])]
            elif D < 0:
                return []
            else:
                return [(-self.polynomial[1] - D ** 0.5) / (2 * self.polynomial[2]), (-self.polynomial[1] + D ** 0.5) / (2 * self.polynomial[2])]

            