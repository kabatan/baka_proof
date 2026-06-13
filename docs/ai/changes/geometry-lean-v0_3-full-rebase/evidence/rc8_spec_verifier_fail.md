# RC8 spec verifier result

Status: FAIL_FIXABLE

Reviewer: spec_verifier

## Findings

```text
The release acceptance and evaluation matrix did not yet enforce all v0.3
release requirements. Required metrics were missing from matrix outputs, and
the release script could pass without verifying the 25-entry Level2 pilot
corpus and complete metric set.
```

```text
The final closure claim exceeded available evidence because model-backed
GenesisGeo/TongGeometry provider evidence was not available.
```

## Remediation Status

```text
Evaluation matrix outputs now include the required metric keys and 25-entry
benchmark accounting.

Release acceptance now fails/blocks when model-backed provider evidence is
missing or closure claims exceed evidence.

The current release report is blocked, not passed.
```
