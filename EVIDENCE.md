# Evidence and the claims it supports

The theorem concerns each fixed known k=2,3,5/2, every known N0>0, positive rates and states, and exact derivatives at one time. J4 has five components; J5 has six.

| Claim | Evidence | Role and limit |
|---|---|---|
| J5 identifies a generic true point against every positive same-k competitor | Article Proposition 4 (`prop:upper`); Demin–Pogudin–Rackauckas v3, Theorem 4.12 / Remark 4.18; companion preprint Sections 2–5 | Prose application of existing observation-field theory, also explained by an elementary separant argument in Section 2. The common output denominator is nonzero for every competitor sharing the true jet. It is not a finite numerical extrapolation. |
| Three positive same-J4 pairs | `producer/output/certificate.json`, two saved algebraic check results | Quartic root isolation, positivity, original-ODE jets and exact remainder identities. No approximate equality is accepted. |
| Both full J4 Jacobians are nonzero | `producer/output/certificate-check.json`, `independent/source-certificate-check.json` | Five-variable derivatives at both points. One checker uses elimination in the determinant; the other uses a permutation sum in separately written arithmetic. |
| Ambiguity holds on a nonempty open set | Article Lemma 6 (`lem:two-branches`) | Inverse function theorem at two disjoint regular inverse branches. Does not assert ambiguity at every point or exactly two points in every fiber. |
| Generic local least order is four | Article proof of Theorem 2 | A nonzero J4 determinant and the dimension/constant-rank obstruction for m<=3. |
| Every N0>0 is covered | Article scaling equation | Positive population scaling preserves admissibility, jet equality and regularity. |
| Additional ambiguity examples | Seven interval records in `independent/stage1-certified-pairs.json` and `independent/extra-pairs.json` | Five first-stage exponents and two changed-point certificates at 7/2,1+sqrt(2). The main theorem is not extended to those two exponents here. |

The first three algebraic certificates have true coordinates (alpha,gamma,S0,I0,h0)=(1,1,2,1,1), h0=1/Z0, N0=10. Their true full-Jacobian determinants are 16, 1467/8 and 9495/128. The alternate points have rho=alpha/(1+alpha I0) equal to the unique real root in the stored rational interval and gamma equal to the stored polynomial evaluated there.

The certificate JSON uses `q` for the continuous coordinate rho in its description; this is unrelated to the integer denominator q of k=p/q in the article. Each quartic has exactly one real root in (0,1), as checked by the separate Sturm implementation; this is not a complete count of all positive ODE candidates.

The article's reduced gamma polynomials are exact remainders modulo those quartics. `build_tables.py` reproduces them and broadens exact stored interval bounds outwards, including the displayed alternate alpha, gamma, S, Z and R coordinates. Displayed decimals are rational enclosures. `article-cases.json` and `certificate-tables.tex` are regenerated and compared during default verification.

The interval evidence uses a separate polynomial-state recurrence in (y,s,b,rho,g), where s=S*b. After fixing y,y',y'', the remaining two-dimensional residual map determines y''' and y^(4). An invertible rational preconditioner C gives a map a-C*F(a)+(Id-C*F'(B))*(B-a) strictly inside its rational box, with derivative infinity norm less than one. Existence and uniqueness in that box follow from the contraction theorem. Positive-coordinate bounds and determinant bounds are part of each certificate. For 1+sqrt(2), rational endpoints enclosing sqrt(2) are checked by squaring, and the calculation holds uniformly throughout the k interval.

`verify_intervals.py` recomputes every exact field of the frozen interval certificates. It does not rerun the historical floating-point search. The exploratory output is retained to document selection; it is not used to accept an identity. The original extra-pair script includes a surplus determinant check at rho=1/2; the changed true point is rho=2/5, and the replay explicitly recomputes that true-branch determinant.

These finite checks support the certificate lemma. The all-competitor upper bound, the open-set argument and the scaling step are mathematical arguments in the article; a stored PASS flag alone is not their proof.
