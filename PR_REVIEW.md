PR: Add extracurricular activities management and participant functionality

Summary of review:

- Functionality: Good additions — signup/unregister endpoints and front-end UI are implemented.
- Tests: Added TestClient tests that cover signup and unregister flows. Tests pass locally.

Actionable suggestions:

1. Use Pydantic models for request validation (added in follow-up).
2. Isolate test state using fixtures (added in follow-up).
3. Split runtime and dev/test requirements into separate files.
4. Consider persistence or note that in-memory `activities` is ephemeral.
5. Replace browser alerts with non-blocking UI feedback and use an SVG icon for delete.

CI:
- Added GitHub Actions workflow `.github/workflows/pytest.yml` to run pytest on push/PR.

Tests:
- All tests pass locally (`pytest -q` -> 4 passed).

Reviewer's recommendation:
- Address test isolation and validation (done here). Consider splitting dev deps and improving frontend UX. Otherwise ready to merge for demo purposes.
