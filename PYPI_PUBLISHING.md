# Publishing to PyPI

This repository is configured to publish `dream11-integer-optimisation` to PyPI through GitHub Actions using PyPI Trusted Publishing. No long-lived PyPI API token is stored in GitHub.

## One-time PyPI setup

1. Create or sign in to a PyPI account.
2. Open **Your projects** and choose **Publishing**.
3. Add a new pending trusted publisher with:
   - PyPI project name: `dream11-integer-optimisation`
   - GitHub owner: `sauravsingla`
   - Repository: `Dream-11`
   - Workflow name: `publish-pypi.yml`
   - Environment name: `pypi`
4. In the GitHub repository, open **Settings → Environments** and create an environment named `pypi`.
5. Optionally add a required reviewer to the `pypi` environment so publishing requires manual approval.

## Publish version 1.0.0

1. Confirm all tests pass on the default branch.
2. Confirm `pyproject.toml` contains `version = "1.0.0"`.
3. Create and publish a GitHub release tagged `v1.0.0`.
4. The `Publish package to PyPI` workflow will build the source distribution and wheel, run `twine check`, and publish them to PyPI.
5. Verify installation in a clean environment:

```bash
python -m venv .venv-pypi-test
source .venv-pypi-test/bin/activate  # Windows: .venv-pypi-test\Scripts\activate
python -m pip install --upgrade pip
pip install dream11-integer-optimisation==1.0.0
```

## Future versions

PyPI does not allow replacing an uploaded version. For every later release:

1. Increase the version in `pyproject.toml`, for example `1.0.1`.
2. Update `CHANGELOG.md`.
3. Publish a matching GitHub release such as `v1.0.1`.

## Security

Do not add PyPI passwords or API tokens to repository files. Trusted Publishing uses short-lived OpenID Connect credentials issued only for the configured GitHub workflow and environment.
