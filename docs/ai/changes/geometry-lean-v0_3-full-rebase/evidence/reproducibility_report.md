# Reproducibility report evidence

Command:

```text
python scripts/generate_repro_report.py --run-dir runs/geometry_level2_pilot
```

Observed report:

```text
report_id: reproducibility_report:geometry_level2_pilot
run_id: geometry_level2_pilot
replay_status: restored
missing_components: []
restored_components:
  - selected_implementations
  - provider_manifest
  - controller_strategy_log
  - final_verification_state
  - evaluation_funnel
  - level2_run_matrix
```

Artifact:

```text
runs/geometry_level2_pilot/reproducibility_report.json
```

Claim ceiling:

```text
This report supports replay of the Level2 pilot matrix run. It does not imply
Level2 advantage, arbitrary LeanGeo support, or open-problem solving.
```
