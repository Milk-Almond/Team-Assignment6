# Local verification of the proposed addition

Executed October 27, 2026. These commands run locally without model or API calls.

## python3 tools/check_frozen_core.py

Exit 0.

```text
FROZEN CORE INTACT
```

## python3 agents/diffusion_agent/tests/check_contrast.py

Exit 0.

```text
REFERENCE CHECK PASSED: stable external findings and five factors; distinct context and timing text; adoption boundary retained
LIMIT: authored examples and different text do not establish materially different decisions or fresh model behavior
```

## python3 agents/diffusion_agent/tests/check_independent_runs.py

Exit 0.

```text
INDEPENDENT RUN CHECK PASSED: 3 conversations preserved; runs 2-3 valid; run 1 syntax failure retained; shared analytical boundary confirmed
```

## python3 agents/diffusion_agent/additions/v1_1/tests/test_additions.py

Exit 0.

```text
test_frozen_files_unchanged (__main__.AdditionsTests.test_frozen_files_unchanged) ... ok
test_full_register_reaches_every_packet (__main__.AdditionsTests.test_full_register_reaches_every_packet) ... ok
test_identical_timing_fails_legacy_reference_checker (__main__.AdditionsTests.test_identical_timing_fails_legacy_reference_checker) ... ok
test_manifest_hashes_match_actual_artifacts (__main__.AdditionsTests.test_manifest_hashes_match_actual_artifacts) ... ok
test_nested_type_and_extra_top_level_are_rejected (__main__.AdditionsTests.test_nested_type_and_extra_top_level_are_rejected) ... ok
test_only_posture_changes_after_evidence_injection (__main__.AdditionsTests.test_only_posture_changes_after_evidence_injection) ... ok
test_preserved_failed_run_prepares_retry_without_overwrite (__main__.AdditionsTests.test_preserved_failed_run_prepares_retry_without_overwrite) ... ok
test_retry_cannot_overwrite_raw_response (__main__.AdditionsTests.test_retry_cannot_overwrite_raw_response) ... ok
test_retry_exhaustion_requests_human_review (__main__.AdditionsTests.test_retry_exhaustion_requests_human_review) ... ok
test_valid_response_passes_full_contract (__main__.AdditionsTests.test_valid_response_passes_full_contract) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.194s

OK
```

## python3 agents/diffusion_agent/additions/v1_1/scripts/build_packets.py

Exit 0.

```text
Built 3 fixed-evidence packets; no model was called.
```

All six original responses and all three original cases were compared byte-for-byte with the reviewed GitHub snapshot and remain unchanged. Frozen files match the supplied manifest. Ten regression tests passed. Generated packets and manifests include the source register; the source snapshot is preserved rather than re-verified.

No fresh v1.1 model responses or successful model repair have been produced. The existing independent-run check validates preserved artifacts; its printed conversation count is not independent authentication of their provenance. Human team acceptance remains pending.
