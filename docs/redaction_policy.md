# Redaction Policy

Status: V1.5 prototype redaction metadata only.

## Purpose

The redaction layer describes what would need to happen in an external secure system if sensitive material were detected. It does not perform real-data redaction inside this repository.

## Repo Rule

If sensitive markers are found, repo ingestion is denied. The system must not create a redacted copy of real sensitive evidence inside the repository.

## Prototype Redaction Plan

The redaction plan can record:

- fields that would need removal
- fields that would need hashing
- fields that would need generalisation
- denied marker categories
- warnings and non-claims

It must not output original sensitive values.

## Synthetic Evidence

Synthetic mock evidence may be generalised for readability, but it remains mock workflow data only.

## Non-Claims

This is a prototype redaction plan only. It is not legal, privacy, cybersecurity, evidentiary, forensic, Treasury, ATO, tax, or audit validation.
