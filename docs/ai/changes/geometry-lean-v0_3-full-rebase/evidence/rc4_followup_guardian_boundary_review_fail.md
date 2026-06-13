# RC-4 follow-up Guardian boundary review

Reviewer: guardian_boundary_reviewer

Result: FAIL_FIXABLE

Reviewed commit:

```text
0c9a6df V03 full rebase fix RC4 target extraction gaps
```

Remaining blocking findings:

```text
1. TargetLibraryManifest target_library_id must be LeanGeoSubsetV1, not
   LeanGeoSubsetV1:1.0.0; schema must match that exact Base identity.
2. TargetLibraryManifest hash refs are stale after mapping edits, and
   namespace_map_ref lacks a corresponding namespace map artifact.
3. GeometryLevel2Pilot categories must match Base R-EVAL-001 exactly:
   10 simple symbolic closure, 5 auxiliary-construction, 5 proof-worker-only
   baseline, and 5 safe-reject/blocker tasks.
```

Resolved findings preserved:

```text
Lean grammar Plan path exists and lake builds from lean/.
Construction mappings include required fields.
Raw/non-elaborated text with a nonempty anchor safe-rejects.
Claim spec schema requires provenance hashes.
Extraction mutation families are covered.
```
