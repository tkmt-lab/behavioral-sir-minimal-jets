# Verification record

Release edition: article 1.0 / packet 1.0.0, dated 10 November 2026. Initially prepared on 27 October 2026 as an unpublished candidate. The initial article received a MINOR report from an AI reviewer, with one required bibliographic correction. The correction and all optional presentation suggestions were addressed on 27 October 2026; confirmation was pending in that pass. No separate confirmation of that initial review was recorded as of 5 November 2026. There is no human expert review or proof-assistant formalization.

## 27 October 2026: producer computation and proof

The producer fixed three initial points and examined the exponents 2,3,5/2. The first two points had one positive candidate in the pilot, while the third had two. The theorem uses the third point's two regular positive branches and does not require the full nine-case pilot classification. SymPy elimination was used to construct the candidates. The distributed certificate proof does not assume the correctness of that elimination: it checks the resulting points directly in the original ODE.

The producer then wrote a standard-library Fraction checker importing no CAS or elimination code. It implements Sturm root counts, rational polynomial quotient arithmetic, Euclidean inverses, rational interval positivity, a Taylor recurrence in (S,I,h), and dual-number differentiation with respect to (alpha,gamma,S0,I0,h0). It verifies identical derivatives of orders 0–4, different fifth derivatives, and nonsingular 5-by-5 Jacobians at both points. The alternate determinant and fifth difference are coprime to the quartic modulus.

The exact true determinants are 16,1467/8,9495/128. The certificates and full reduced remainders are preserved unchanged. The author's separate implementations at this stage are not described as a separate-agent review.

## 27 October 2026: separate proof and certificate review

The supplied review first fixed a derivation and interval computations before reading the producer proof or new saved certificates. The reviewer had previously worked on the companion fixed-known-k model, so this was not a context-free blind check. The first-stage computation introduced a fresh polynomial ODE in (y,s,b,rho,g), built Taylor recurrences and two-variable derivatives, and certified positive branches using rational interval contraction bounds.

The first stage was frozen at commit c62ba0a47. Its chosen point (alpha,gamma,S0,I0,Z0)=(1,1,2,1,1) happened to coincide with the producer's third point, discovered only when the producer records were read later; it is not counted as a distinct-point check. The reviewer additionally used alpha=2/3 with the other coordinates fixed at k=7/2 and 1+sqrt(2). These are not obtained merely by scaling the original population.

In the second stage the reviewer read producer documents and saved JSON at commit a4fcc3f75d7cfc8c972a2a4e579a705edabbc8cc. It did not read, import or execute the producer's candidate generator or checker. It wrote its own polynomial quotient/Sturm implementation, five-variable automatic derivatives and a permutation-sum determinant, using its earlier polynomial-state ODE recurrence. All five J4 residuals vanished; fifth differences and alternate Jacobians agreed exactly with the producer remainders, were coprime to the quartic, and had intervals excluding zero. Positive bounds were checked for all required rates and states. The algebraic roots also lay inside the earlier frozen interval boxes.

The review supported all six requested components: the known J5 upper bound and all-positive-competitor passage; three positive same-J4 pairs; Sturm isolation; nonsingularity of both branches and the nonempty-open ambiguity argument; the dimension-based local lower bound; and scaling to every N0>0. It found no required mathematical correction. It did not repeat the complete nine-case elimination pilot, which is not needed for the theorem.

## 27 October 2026: article review and corrections

An AI reviewer reviewed the initial article and packet on 27 October 2026, reporting MINOR with one required correction to the OPT DOI. The review report is 12,477 bytes, SHA-256 `7695d6e20401d6f06f5b1fa5cecb8bf8bd96b3d30bc89ddca4723334afe95257`. It read the manuscript and saved results, rederived selected expressions by hand, and reported approximate hand calculations. It did not execute the certificate programs or consult the external papers, and had prior experience reviewing the companion articles. Its statements are an AI review, not human peer review or a newly executed verification run.

The research-side correction pass verified the OPT reference against the Springer publisher page and changed the DOI to `10.1007/s00200-021-00486-8`. The report's optional suggestions were accepted: an elementary separant explanation of the existing fifth-order bound; explicit order/component counting and the q=1 coordinate change; the removed true-point factor and the stored Sturm count on (0,1); and a table of outward rational coordinate enclosures. The legacy `q`/rho notation is explained in EVIDENCE.md. Mathematical claims and sealed certificates remain unchanged. See REVIEW-RESPONSE.md; the revised text awaited confirmation in that 27 October pass.

## Source connection recorded on 27 October 2026; display updated on 6 November 2026

Demin–Pogudin–Rackauckas, arXiv:2609.06134v3, Theorem 4.12 and Remark 4.18 were checked directly in the supplied review and reread from the same-day primary-source cache during article preparation. In the no-input rational cover there are two states and three constant parameters. Taking the ground subfield E=C yields observation-field generation by J5. Supplying the unknown parameter field in advance would change the question. Remark 4.15 explicitly allows the general upper bound not to be minimal.

The companion version 3.0, Sections 2–5, supplies observability of alpha,gamma,beta^q,S,I on the rational cover. The q=1 integer recovery formulas and the q=2 complex sign ambiguity are kept distinct. Positive real roots recover beta uniquely. For each observable quantity, a rational expression in J5 can be chosen. Its denominator is a function of the common jet, so a competitor with the same jet shares its nonzero value. Cleared identities then apply at all positive competitors; the competitor is not required to satisfy an independent genericity assumption. The finite product of denominators is nonzero on an open dense set in every admissible positive domain. No expanded J5 inverse was computed.

The companion is article 3.0 of 27 October 2026, supplied as a publication display edition dated 10 November 2026. In the second reader-text pass on 6 November 2026, only its title-page edition label changed in TeX, and the PDF was rebuilt. The later contents clarification on the same date is recorded below. Mathematical text and numbering are preserved. source-derivatives.json records original and display-edition fingerprints. The original TeX/PDF are preserved in the private preparation archive. The inherited verification history concerns the original mathematical text; this display change is not a new proof or a DOI assignment.

## 27 October 2026: literature comparison and external software

The bounded literature comparison read the producer result at commit 55892a7676b81d32e1f2e17be1a3cb85b127c6be, before the later separate mathematical review. It identified the contribution as the positive regular two-branch certificate making order five minimal for the three exponents. Finite-generation theory, the fifth-order upper bound and the local rank method themselves are prior work. No matching result with the same positive domain and quantifiers was found in the examined materials; this is not a priority claim or exhaustive search of unpublished work.

The literature reviewer examined the original supplement, later theory, author-model code and software documentation. SIAN Maple commit a25124333e55d39fae16e31da844180f465afc9c and StructuralIdentifiability.jl commit 1b55b35a1365d4dcf181362aab9e78efe52231a1 were read statically. **Neither software package was executed.** In particular, a Julia precision setting of five describes coefficients of orders 0–4 in the inspected local-rank code, not an executed fifth-derivative comparison. Generic complex classifications, positive real competitors, sufficiency bounds and minimality are different outputs.

## Portable reproduction recorded through 6 November 2026

The input list in source-derivatives.json records original sizes and hashes under neutral original-input identifiers, alongside packaged paths, hashes and change descriptions. The producer certificates, mathematical results and formulas are preserved. check_source_certificate.py reads the same sealed data from producer/output and uses those packet-relative paths in its receipt. An exploration docstring and a resource-limit diagnostic use public descriptions. The receipt differs only in its source keys; mathematical fields and the original input-commit label are preserved. The companion changes are described above. The private preparation archive retains the original path mapping.

The packaging-stage verify_intervals.py imports the original interval formulas and replays the frozen rational boxes. It validates the exponent intervals, strict contraction, positive reconstruction, separation from the true point, both determinants and the fifth-derivative gap. It performs no numerical search. The old numerical solver remains as the helper originally used by the review, and its exploratory log is preserved. Replaying that helper or the frozen certificates is reproduction, not a new independent derivation.

The default verify.py runs in an isolated temporary copy and compares all mathematical fields with the sealed results. It ignores only seconds, rss_bytes and max_rss_bytes. The separate algebraic checker runs before the producer receipt is regenerated, so its input fingerprint remains that of the sealed receipt. Article polynomial/table generation is checked byte-for-byte. No external service, package installation, SIAN or Julia execution is involved.

The historical programs use 60-second alarms. The producer guard monitors peak RSS against 2 GiB; the original reviewer programs record RSS and one has a 512 MiB check, but this is not an OS-enforced memory cap. The 27 October 2026 clean-copy run used OS-level network blocking and checked the file inventory before and after execution. Its report retained runtime measurements and the tested packet hash. That network-blocking statement describes that run only. No GitHub CI run was recorded in the 27 October or 5 November research preparation passes.

The manuscript separates mathematics from these process records. Subsequent article review, any scope changes and any publication operations require their own records.

## 5 November 2026: blind-review response and local replay

The blind review read only the article TeX/PDF and generated table input, independently checked the main three certificates and lower bounds, and left the upper bound conditional on equation (5). Its report SHA-256 is `c55e77e6f967db44e2907df9d66b13e28880df84fb03081d466f2f50355c6585`. It did not read the companion or certify the supplementary interval records. The Dated responses to review items section below gives an item-by-item disposition.

The author-side revision added Lemma 3 and Appendix B. The latter proves cover observability directly: rational constant field K; irreducibility and normalization of Q; independence of all but one output monomial over K; Wronskian inversion yielding coefficients in the observation field; and parameter/state recovery. The existing separant argument then places those quantities in the fifth-order field. Companion Lemma 3, Lemma 4, Propositions 5--6 and equations (11)--(13),(16) provide the exact source correspondence. The companion was unchanged in that 5 November pass. The current bibliography and claims.json identify the publication display edition described above.

check_observability.py separately differentiates the rational cover in a sparse Laurent-polynomial ring over Fraction, and checks the unpowered relation, powered Q identity, S-recovery identity, unit normalizing coefficient and recovery coefficients symbolically for all three exponents. It parses the printed root intervals and uses the existing separate algebraic checker's Sturm implementation to count one root in each. observability-check.json is its deterministic receipt. It does not evaluate or numerically claim nonvanishing of the Wronskian; that nonvanishing follows from the prose constant-field and minimal-polynomial proof. This check is an author-side algebraic check, not an independent-agent proof review.

The revised verify.py replayed this additional receipt after the two original algebraic implementations, seven stored interval records and table regeneration, in a disposable copy of the closed inventory. During that 5 November pass, the original sixteen source-derivative records, all sealed mathematical data and companion files remained byte-identical. check_packet.py also verifies the complete PROVENANCE inventory, fixed companion fingerprints, article labels and current PDF validation. PDF layout validation is recorded in pdf-validation.json. No external identifiability package, remote CI, external submission, push or publication operation was performed in that author-side revision pass on 5 November 2026. Independent confirmation of the added proof was pending at the end of that pass.

## 5 November 2026: subsequent limited Appendix B blind review

On 5 November 2026 a separate blind review returned PASS for Lemma 3, Appendix B, the Section 2 finite-jet reduction and Proposition 4, for (p,q)=(2,1),(3,1),(5,2). It found no required correction in that scope. It did not audit the whole article, rerun the lower-bound certificates or review external sources. The reviewed TeX, table and PDF SHA-256 values were respectively `b6518be8359b1d5c3a1b83055f1adc27e1231eaadb5a24d1acbfb5b2668194c9`, `e00ad10998c48ddd73197e60651a14895d33a4d08421fc53c3d70c42e9a31bd7`, and `e6da45a297572e54b497785eaa23c14d453ef377b8cdb2fddb4b0c3be6047e95`. Relative to that reviewed TeX, this release changes the article date line and companion bibliography display and hashes; that review is not a review of a later mathematical revision. The review report SHA-256 is `fdf52a41fc741545a9bd923d138c202772a8d1b9aa9780d6060eb374b3bbdb9d`. No separate confirmation of the initial AI article-review corrections was recorded as of 5 November 2026; no human peer review is claimed.

## 5 November 2026: release presentation preparation

The release-edition metadata is dated 10 November 2026. This pass changed presentation and metadata, rebuilt the main PDF and renewed hashes; it preserved the mathematical TeX body, generated tables, all sixteen source-derivative files and fixed companion bytes. The README commands were rerun in a fresh copy, as recorded in the research preparation report. This pass did not perform an external publication or DOI operation. The release date is edition metadata, not evidence of an upload.

## Publication display and portable provenance, 6 November 2026

The second reader-text pass replaced internal source names with public input identifiers and packet-relative paths, updated the companion title-page label and bibliography, rebuilt both PDFs, and renewed current fingerprints. The original companion bytes and source-name correspondence are retained in the private preparation archive. Mathematical TeX bodies, formulas, certificate values and claim scopes are preserved. Earlier reviewed fingerprints remain historical records. That pass expanded the public-content scan to cover internal identifiers and relative research paths as well as known absolute paths, including extracted PDF text and metadata.

## Dated responses to review items

### 27 October 2026: item-by-item responses

Release edition: article 1.0 / packet 1.0.0, dated 10 November 2026. This response was first prepared for the unpublished candidate on 27 October 2026. The AI article-review report was MINOR, with one required bibliographic fix. All suggestions below were adopted. The theorem, its quantifiers and the sealed certificates are unchanged. This response records the research-side changes, not referee approval of the revised article.

| Review item | Response and reason |
|---|---|
| 1: OPT DOI (required) | Corrected to `10.1007/s00200-021-00486-8`. The [publisher's page](https://link.springer.com/article/10.1007/s00200-021-00486-8) matches the title, authors, volume 34(2), pages 165–182 and year 2023. The cited arXiv version and theorem numbers are unchanged. |
| 2: Elementary fifth-order argument | Added a paragraph in Section 2: at the first algebraic derivative step the nonzero separant makes the generated field stable under differentiation; transcendence degree five bounds that step by order five. This explains the same upper bound, retaining the DPR attribution and companion observability dependency. |
| 6: Quartic origin and Sturm count | Explained that the known true-point factor `2*rho-1` is removed from the degree-five elimination polynomial before the quartic. The saved factor identity was checked exactly. Stated the independently checked single root in (0,1), while retaining the limit on counting all positive candidates. |
| 7: Alternate coordinates | Added outward rational enclosures for alpha, gamma, S, Z, R from the unchanged certificate receipt, generated and checked with the article tables. The table shows the positive second branch concretely. |
| 8: Presentation | The theorem now states that J4 has five numbers and J5 six. Section 2 identifies q=1 as the original model with z=1+alpha*I. EVIDENCE.md explains the historical q/rho naming in certificate.json. |

The input report is 12,477 bytes with SHA-256 `7695d6e20401d6f06f5b1fa5cecb8bf8bd96b3d30bc89ddca4723334afe95257`. Its scope and prior model context are recorded in this record. The report did not execute programs or consult external papers. Correction-stage reproduction is recorded separately; it is not another independent review. No human expert review, formal proof, SIAN/StructuralIdentifiability.jl run, or remote CI run is claimed. Confirmation of the revised article and publication review were pending in the 27 October 2026 correction pass; no separate confirmation of that initial review was recorded as of 5 November 2026.

### 5 November 2026: item-by-item responses

The blind report independently reconstructed the three main algebraic certificates and the fourth-order lower bounds, but reviewed only the article, PDF and generated table input. It therefore left the fifth-order upper bound conditional on equation (5); it did not allege an error in the companion. Its supplementary numerical check was not an interval-certificate review. The report fingerprint is SHA-256 `c55e77e6f967db44e2907df9d66b13e28880df84fb03081d466f2f50355c6585`.

| Item | Disposition |
|---|---|
| R1: cover statement and rational first-integral hypothesis | Adopted. Section 2 states Lemma 3 on the complex rational cover. Appendix B proves that the rational constant field is exactly the parameter field, and proves the minimal output relation. This supplies the hypothesis used by OPT Theorem 4.7 in the companion. |
| R1: coefficient observability and state recovery | Adopted. Appendix B uses a nonzero Wronskian to express normalized output-relation coefficients directly in the observation field, then gives recovery coefficients separately for k=2,3 and 5/2 and the rational expression for S. The existing differential-field argument subsequently reduces the required derivative order to five. No inference from positive-domain identifiability to complex-cover field membership is assumed. |
| R1: exact companion locations | Adopted. Companion Lemma 3, Lemma 4, Propositions 5--6, Section 4 equations (11)--(13) and Section 5 equation (16) are explicitly identified. Its Theorem 2 is distinguished from the field statement needed here. |
| R1: fixed bundled dependency | Adopted. The 5 November bibliography printed both full SHA-256 hashes of the unchanged companion TeX and PDF. The current bibliography, claims and inventory identify the publication display edition; source-derivatives.json retains the original fingerprints. |
| R1: permanent public URL | In the author-side revision of 5 November 2026, a permanent public URL or DOI for the companion had not been assigned. That pass preserved its exact bytes and full hashes. The current bundle contains the publication display edition described in this record; no companion DOI is asserted. |
| R2: printed isolating intervals | Adopted. Section 3 and Appendix A define each alternate root by the printed interval. The additional checker parses those actual intervals, proves each contains exactly one root by Sturm's algorithm, and checks that the unchanged sealed interval lies strictly inside. Section 3 gives the packet verification command and checker names. |
| R3: supplementary certification inputs | Adopted. Section 5 names both interval JSON records and their root_box_p_q, k_interval and preconditioner fields; it explains the historical coordinate names and gives the interval replay command. These records remain supplementary, outside the three-exponent main theorem. |
| Abstract quantifiers | Adopted. The abstract specifies an open dense true set for generic global identification and a nonempty open ambiguity set at order four, with no density assertion for the latter. |
| Dependent R0 | Adopted. A sentence immediately after Theorem 2 identifies R0 as dependent and counts five independent unknown coordinates. |
| Positive root choice | Adopted. Section 2 explicitly distinguishes the positive conclusion from the complex or signed domain. |
| Nonsingular Jacobian and stability | Adopted. Section 5 states that local invertibility supplies no condition-number or noisy-estimation guarantee. |

The correction-stage symbolic identities and printed-interval checks use only the standard library. Both original algebraic checkers and all seven stored rational interval certificates are replayed by verify.py. The first-integral, minimality and Wronskian arguments are prose mathematics; finite checks do not replace them. This is the research team's revision and reproduction, not another blind or independent-agent review. Independent confirmation of the revised Appendix B and publication approval were pending in that author-side pass on 5 November 2026. See the subsequent limited blind-review result above. Main theorem scope, original certificate data and companion bytes were preserved in that 5 November pass.


## 6 November 2026: provenance metadata consolidated

The packet metadata had carried the following input and revision identifiers. They were retained here when the edition metadata was shortened.

```json
{
  "date": "2026-10-27",
  "input_commit": "5fd0f5ab545ddab3b5915d2cd720eb32176717c6",
  "revision_input_commit": "7cb9957ecc4c79c55f667f5fbb89b370bd096446",
  "independence": "Separate pre-reading derivation and code with prior companion-model context; packaging replay is not a new independent review.",
  "blind_revision_input_commit": "4ce4fad31",
  "blind_revision_date": "2026-11-05",
  "release_presentation_date": "2026-11-05",
  "text_revision_input_commit": "5002f42851f70ad1db3469b71caa71b966d9c5ce",
  "text_revision_date": "2026-11-06",
  "second_text_revision_input_commit": "d88556dc3fc898310f0869f42945c85c810ecf21",
  "second_text_revision_date": "2026-11-06"
}
```

The earlier PDF validation chain was preserved as follows. These fingerprints identified earlier files, rather than the current distribution.

```json
{
  "date": "2026-11-06",
  "source_sha256": "f544b60f2219186eb2e730015cc935d2b1d7e6fec282a546d97969ac5f7b53d4",
  "pdf_sha256": "be8e2383e545c785cec9860f759192d1552da9da93f3c63df1dc0bbcff7f83c5",
  "build": "pdfTeX 3.141592653-2.6-1.40.26 (TeX Live 2025/dev/Debian), two pdflatex passes, -no-shell-escape; SOURCE_DATE_EPOCH=1793923200; Poppler rendering",
  "previous_validation": {
    "date": "2026-11-05",
    "source_sha256": "f544b60f2219186eb2e730015cc935d2b1d7e6fec282a546d97969ac5f7b53d4",
    "pdf_sha256": "ee1535125ff05ed81f06b791a24379927ce65904ef7588a5300d1e5939a90b03",
    "build": "pdfTeX 3.141592653-2.6-1.40.26 (TeX Live 2025/dev/Debian), two pdflatex passes, -no-shell-escape; Poppler rendering",
    "previous_validation": {
      "date": "2026-11-05",
      "source_sha256": "b6518be8359b1d5c3a1b83055f1adc27e1231eaadb5a24d1acbfb5b2668194c9",
      "pdf_sha256": "e6da45a297572e54b497785eaa23c14d453ef377b8cdb2fddb4b0c3be6047e95",
      "build": "Tectonic cached-only; original eight-page inspection retained in input commit"
    }
  }
}
```

## 6 November 2026: final reader-text cleanup

The final text pass removed an internal literature rating while retaining the bounded comparison and its lack of a priority claim. It consolidated review responses, revision identifiers and earlier PDF validation fingerprints in this record, and shortened the edition metadata and changelog. Internal reviewer labels were replaced by descriptive roles. The mathematical TeX, certificate data, formulas and numerical values were preserved.

The earlier edition metadata had recorded no upload or DOI assignment in the 5 November 2026 pass. It had listed confirmation of the initial article-review corrections, a review of publication prerequisites and a publication decision as remaining at that time. Those were historical workflow states, not scientific conditions or a statement that a later upload occurred.

The final pass rebuilt both PDFs, refreshed current fingerprints and ran the README instructions in a fresh copy. It used local computations without an OS-level network block; it performed no external publication or DOI assignment. The edition date remained 10 November 2026 and the DOI field remained unassigned.

## 6 November 2026: companion contents clarified

The reader-text correction clarified three references in the companion display TeX: its verification-record reference, the finite-field matrices and minors, and the missing-factor negative control. These referred to the original companion supplement, while this packet contained only the companion article TeX and PDF. A contents guide was added in companion/README.md and linked from both main READMEs. The guide distinguished the original supplement and verification record from the minimal-jet packet and stated the limits of local reproduction. No public URL or DOI for the original supplement was supplied in this pass.

The correction preserved all mathematical statements, formulas, numerical values and theorem/equation numbering. It rebuilt both PDFs and refreshed their current fingerprints and dependent references; original source and earlier review fingerprints remained historical identifiers.

The preceding PDF layout record had reported: "On 6 November 2026, the second text pass inspected all 17 pages. The final text pass compared all 17 rendered pages against that edition: 16 were pixel-identical; the main bibliography page differed only at the companion PDF fingerprint and was inspected again. No clipping or overlap was found." That process description was moved here from the current layout metadata.

The correction pass inspected all eight main-article pages and all nine companion pages after rendering the rebuilt PDFs, and found no clipping, overlap or unresolved references. The contents guide was checked against Section 9 (Exact finite checks) of the companion. These were author-side text and layout checks, not a new mathematical review.
