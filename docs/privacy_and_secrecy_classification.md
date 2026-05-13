# Privacy and Secrecy Classification

Status: V1.5 prototype classification scaffolding.

## Purpose

The classification layer gives synthetic evidence packets a first-pass privacy and secrecy label so review workflows can flag sensitive mock scenarios. It is not an official government protective marking scheme.

## Prototype Classifications

Privacy classifications:

- `public`
- `low`
- `moderate`
- `high`
- `restricted_placeholder`

Secrecy classifications:

- `open`
- `internal_research`
- `confidential_placeholder`
- `restricted_placeholder`

## Prototype Rules

- Public aggregate data can be `public` / `open`.
- Firm-level financial data is at least `moderate` / `internal_research`.
- Worker-level wage or hour evidence is `high` / `confidential_placeholder`.
- Transfer-pricing contracts and related-party records are `high` / `confidential_placeholder`.
- Detected sensitive markers are `restricted_placeholder` and require review.

## Forbidden Markers

Mock packets are rejected if they contain markers such as TFN, tax file number, passwords, API keys, private keys, bank-account references, Medicare numbers, real taxpayer references, or real business ABN markers not explicitly labelled fake.

## Non-Claims

This is prototype classification only. It is not legal, tax, Treasury, ATO, ABS, Fair Work, audit, forensic, privacy, secrecy, or economic validation.

Future real evidence handling requires a separate data-governance design, privacy impact review, legal review, secure storage model, access controls, retention controls, and source-authorisation process.
