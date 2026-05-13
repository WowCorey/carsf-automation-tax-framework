# Ingestion Audit Design

Status: V1.5 immutable-style prototype logging.

## Purpose

The ingestion audit module creates compact hash-based records for ingestion decisions. It is designed to show how decisions could be chained and reviewed without storing raw sensitive request content in audit records.

## Hashing

The prototype uses SHA-256 over canonical JSON for:

- decision reasons
- compact decision metadata
- chained record content

The `record_hash` changes when decision content changes.

## Safety Boundary

Audit records must not include raw sensitive text, real evidence content, credentials, personal identifiers, taxpayer data, or source documents.

## Non-Claims

This is immutable-style prototype logging only. It is not blockchain, legal audit logging, cybersecurity assurance, evidentiary validation, Treasury guidance, ATO guidance, tax validation, or forensic validation.
