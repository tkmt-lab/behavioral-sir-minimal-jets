"""Exact Appendix B identities and printed root intervals, using stdlib only.

This verifies finite algebraic identities. The constant-field, minimality and
Wronskian nonvanishing arguments remain prose proofs in the article.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


class Poly:
    """Sparse rational Laurent polynomials in six indeterminates."""
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = value.terms.copy()
        elif isinstance(value, dict):
            self.terms = {e: F(c) for e, c in value.items() if c}
        else:
            self.terms = {(0,) * 6: F(value)} if value else {}

    def __add__(self, other):
        out = self.terms.copy()
        for e, c in Poly(other).terms.items():
            out[e] = out.get(e, F(0)) + c
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        out = {}
        for e, c in self.terms.items():
            for f, d in Poly(other).terms.items():
                g = tuple(x + y for x, y in zip(e, f))
                out[g] = out.get(g, F(0)) + c * d
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        if n < 0:
            assert len(self.terms) == 1, 'Only monomials may be inverted'
            (e, c), = self.terms.items()
            return Poly({tuple(n * x for x in e): c ** n})
        result = Poly(1)
        for _ in range(n):
            result = result * self
        return result

    def diff(self, i):
        out = {}
        for e, c in self.terms.items():
            if e[i]:
                f = list(e)
                f[i] -= 1
                out[tuple(f)] = c * e[i]
        return Poly(out)

    def coefficient(self, output_powers):
        return Poly({e[:3] + (0, 0, 0): c for e, c in self.terms.items()
                     if e[3:] == output_powers})


def variables():
    return [Poly({tuple(int(i == j) for j in range(6)): 1}) for i in range(6)]


def relation(a, b, g, y, v, w, p, q):
    u = 1 + a * y
    A = y * u * w - (1 - (F(p, q) - 1) * a * y) * v**2 + F(p, q) * a * g * y**2 * v
    Q = u**(p - q) * A**q - (-b)**q * y**(2 * q) * (v + g * y)**q
    return u, A, Q


def main():
    if not __debug__:
        raise SystemExit('Assertions must remain enabled')
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    rows = []
    for p, q in [(2, 1), (3, 1), (5, 2)]:
        a, b, g, S, z, _ = variables()
        y = (z**q - 1) * a**-1
        DS = -b * S * y * z**-p
        Dz = F(1, q) * a * z**(1 - q) * (b * S * y * z**-p - g * y)
        D = lambda f: f.diff(3) * DS + f.diff(4) * Dz
        v = D(y)
        w = D(v)
        u, A, Q = relation(a, b, g, y, v, w, p, q)
        assert not (z**(p - q) * A + b * y**2 * (v + g * y)).terms
        assert not Q.terms
        assert not (S * A + y * u * (v + g * y)**2).terms
        a, b, g, y, v, w = variables()
        _, _, Q = relation(a, b, g, y, v, w, p, q)
        c = Q.coefficient
        assert c((q, 0, q)).terms == Poly(1).terms
        if q == 1:
            expected = [((2, 0, 1), p * a),
                        ((3, 1, 0), p * (p - 1) * a**2 * g),
                        ((2, 1, 0), b + p * a * g)]
        else:
            expected = [((3, 0, 2), 5 * a),
                        ((3, 1, 1), 5 * a * g),
                        ((6, 0, 0), -b**2 * g**2)]
        for powers, value in expected:
            assert c(powers).terms == value.terms, (p, q, powers)
        rows.append(dict(p=p, q=q, unpowered_relation=True, powered_relation=True,
                         state_recovery=True, normalized_coefficient=True,
                         recovery_coefficients=True,
                         output_monomials=len({e[3:] for e in Q.terms})))

    # Parse the actual printed intervals, rather than copying their endpoints.
    table = (ROOT / 'certificate-tables.tex').read_text().split(r'\newcommand{\MainBoundRows}{')[1].split('\n}')[0]
    intervals = re.findall(r'^\$[^\n]+?\$ & \$\(([^,]+), ([^)]+)\)', table, re.M)
    sys.path.insert(0, str(ROOT / 'independent'))
    from check_source_certificate import peval, sturm
    cert = json.loads((ROOT / 'producer/output/certificate.json').read_text())['cases']
    assert len(intervals) == len(cert) == 3
    roots = []
    for record, pair in zip(cert, intervals):
        lo, hi = map(F, pair)
        polynomial = list(map(F, record['polynomial_ascending']))
        assert peval(polynomial, lo) and peval(polynomial, hi)
        assert sturm(polynomial, lo, hi)[0] == 1
        a, b = map(F, record['root_interval'])
        assert lo < a < b < hi and not lo <= F(1, 2) <= hi
        roots.append(dict(k=record['k'], printed_interval=list(pair),
                          unique_root=True, sealed_interval_strictly_inside=True))
    result = dict(status='PASS', symbolic_identities=rows, printed_root_intervals=roots,
                  scope='Exact polynomial identities and Sturm counts; general field arguments are prose proofs')
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
