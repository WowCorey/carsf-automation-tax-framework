# Decision Log Design

Status: V1.5 prototype audit-trail design.

## Purpose

Decision logs record the sequence of model and review steps taken for each example run. They are intended to make the prototype easier to review, reproduce, and challenge.

## Logged Steps

The standard decision log can record:

- evidence assessment
- QLC
- HLE
- AII
- NLTG
- AAVA
- AEL
- ARL
- caps
- safe harbour
- avoidance
- grouping
- transfer-pricing preview
- mixed-unit handling
- mock evidence packet assessment
- review-state workflow transition
- privacy/secrecy classification

## Determinism

Decision logs use deterministic run identifiers and step identifiers. The only intentionally variable field is `generated_at`.

## Data Controls

Decision logs must not include secrets, credentials, personal identifiers, or personal data. They should store compact summaries, not raw payroll, tax, or personal records.

Mock evidence workflow logs should record only synthetic packet identifiers, counts, classifications, review states, warnings, and non-claims.

## Non-Claims

Decision logs are prototype audit trails only. They do not create legal findings, tax findings, Treasury guidance, ATO guidance, forensic findings, audit validation, or economic validation.
