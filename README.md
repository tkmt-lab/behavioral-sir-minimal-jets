# Minimal jet orders in a positive behavioral SIR model

Article **1.0** / certificate packet **1.0.0** · release edition **10 November 2026** · DOI: unassigned.

For each fixed, known **k = 2, 3, 5/2** and known **N0 > 0**, the infectious population I(t) and its exact derivatives at one time identify positive rates and states at minimal jet order **four locally and five globally**, for generic true points.
Global comparison includes **every positive competitor with the same k and N0**.
The positive fourth-order ambiguity certificates help researchers distinguish local identifiability from uniqueness throughout the positive domain.

Quick check (Python 3.10+, from this directory):

```sh
python3 -B verify.py
```

Expected: JSON with `"status": "PASS"`; three main algebraic certificates (k=2,3,5/2), checked by two implementations, and seven interval certificates.

[日本語](README.ja.md) · Author: Tatsuhiko Takimoto · Research contact: [research@tatsuhikotakimoto.com](mailto:research@tatsuhikotakimoto.com)

Repository: https://github.com/tkmt-lab/behavioral-sir-minimal-jets

## Result and evidence

A fourth-order jet contains five numbers: I(0), I'(0), ..., I^(4)(0). A fifth-order jet contains six. Generic means an open dense set of true points in the positive real domain.

The [article](paper-sir-minimal-jets-v1-en.pdf) states the theorem and proof. [claims.json](claims.json) connects each claim to the exact evidence. Lemma 3 and Appendix B supply the cover-observability argument within the article: rational constants, a minimal output relation, direct Wronskian coefficient recovery, and state recovery. The fifth-order upper bound applies the observation-field theorem cited under [Built on earlier work](#built-on-earlier-work). The contribution is the certified positive fourth-order ambiguity at two regular points, which makes that upper bound sharp for the three exponents.

At N0=10 and (alpha,gamma,S0,I0,Z0)=(1,1,2,1,1), each of the three exponents has a distinct positive competitor with the same J4. Both five-dimensional jet Jacobians are nonsingular. The inverse function theorem then gives a **nonempty open set of ambiguous true points**. This prevents J4 from being globally identifying on an open dense set. Positive population scaling transfers the argument to every N0>0.

The package also retains separately produced interval certificates at k=7/2 and 1+sqrt(2), including a changed initial point with alpha=2/3. These supplementary examples support the same fourth-order ambiguity mechanism.

## Reproduce offline

Use Python 3.10 or newer on macOS or Linux. The checkers use the standard library, including the Unix `signal` and `resource` modules. Run with Python assertions enabled.

```sh
python3 -B check_packet.py
python3 -B verify.py
```

The first command checks the closed file inventory, hashes, article labels and scope metadata. The second copies those files into a temporary directory, then runs:

1. The separate algebraic checker on the three sealed producer certificates and receipts.
2. Exact replay of seven stored rational interval boxes through the stored interval formulas.
3. The producer's independent-of-CAS Fraction checker on its three certificates.
4. Regeneration of the article's polynomial and interval tables from the exact stored data.
5. Symbolic Laurent-polynomial checks of the Appendix B relations and recovery coefficients for all three exponents, and Sturm counts in the actual printed root intervals.

Both algebraic implementations verify the original ODE jets, positivity, root isolation, and nonzero Jacobians. They compare all mathematical fields with the sealed records; elapsed-time and peak-RSS fields are omitted from comparison. The original packet stays unchanged.

Optional PDF text/metadata and private-path-pattern checks use existing Poppler commands:

```sh
python3 -B check_packet.py --pdf
```

All three commands return JSON with `"status": "PASS"`. The PDF check also reports `"known_private_path_patterns": "PASS"`. Reproduction uses local files and performs its computations offline.

The supplied PDF can be read alongside the exact checks. To rebuild it, compile `paper-sir-minimal-jets-v1-en.tex` with `certificate-tables.tex` available, using two pdfLaTeX passes with shell escape disabled and an output directory outside this packet. The build and page inspection are recorded in [pdf-validation.json](pdf-validation.json).

## Files and verification

| Location | Contents |
|---|---|
| `producer/` | Three quartic certificates, exact saved results, Fraction checker and resource guard |
| `independent/` | Separately written polynomial-state solver, interval checker, seven interval certificates, algebraic recheck, and historical numerical exploration |
| `verify_intervals.py` | Replay of frozen rational boxes through the original interval formulas |
| `build_tables.py`, `article-cases.json` | Exact conversion of the three certificates into the article's tables and reduced gamma polynomials |
| `check_observability.py`, `observability-check.json` | Exact Appendix B identities and uniqueness of the roots in the printed intervals; the general constant-field and Wronskian arguments are prose proofs |
| [companion/](companion/README.md) | Article 3.0 TeX/PDF extract and contents guide; the guide distinguishes the original supplement from this packet. The needed cover-observability proof is also in Lemma 3 and Appendix B of the main article |
| `VERIFICATION-RECORD.md`, `REVIEW-RESPONSE.md` | Reviewed versions, independence boundaries, literature comparison, review history and responses |
| `source-derivatives.json`, `PROVENANCE.json`, `SHA256SUMS` | Original and packaged fingerprints, presentation changes and closed inventory |

The proof combines prose arguments and exact finite checks by separately written implementations. Running this packet reproduces the stored evidence. [VERIFICATION-RECORD.md](VERIFICATION-RECORD.md) documents the reviewed versions, independence boundaries and review history; [REVIEW-RESPONSE.md](REVIEW-RESPONSE.md) records the responses.

## Scope

The theorem assumes fixed known k in {2,3,5/2}, known N0>0, positive rates and states, and exact derivatives at one time. The supplementary k=7/2 and 1+sqrt(2) certificates do not extend the main theorem. A nonempty open set of fourth-order ambiguity does not imply that every J4 fiber is ambiguous or has exactly two positive points. Classification of all exponents, exceptional points and positive fibers, unknown k or N0, expanded J5 inverse formulas, noisy-data estimation and numerical stability are outside the result.

The proof has not been formalized in a proof assistant or reviewed by human experts. The Appendix B review was limited to the stated proof and fifth-order reduction, rather than a whole-article audit. The bounded literature comparison does not establish priority; external identifiability packages were not executed. The verification record gives the details.

## Version and license

This is the 10 November 2026 release edition, article 1.0 / packet 1.0.0 (tag v1.0.0). The included companion article 3.0 (27 October 2026) has a publication display edition dated 10 November 2026. The source and display editions share the mathematical statements, formulas, numerical values, and theorem and equation numbering; the display text specifies the distribution scope. Their fingerprints are recorded in source-derivatives.json.

Code is Apache-2.0. The article, original text and generated certificate data are CC BY 4.0. The companion preprint carries the same text license. Third-party articles and software are cited through their original sources. See [LICENSE](LICENSE), [CITATION.cff](CITATION.cff) and [version-plan.json](version-plan.json).

## Built on earlier work

Pant, Saucedo and Pogudin supplied the behavioral model and its auxiliary-state formulation. Demin, Pogudin and Rackauckas supplied the observation-field generation theorem used for the fifth-order upper bound (Theorem 4.12 and Remark 4.18). The companion proof uses the identifiability theory of Ovchinnikov, Pogudin and Thompson and of Hong, Ovchinnikov, Pogudin and Yap. The article gives the exact source versions and theorem numbers.

I am grateful to these authors for the model and theory on which this calculation relies. I hope these exact positive-branch certificates provide a useful example for researchers comparing local rank, complex fibers and positive real ambiguity.
