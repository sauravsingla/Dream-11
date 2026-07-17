# Release checklist

Use this checklist before publishing `v1.0.0` and archiving it on Zenodo.

## Data and reproducibility

- [ ] Recover and verify the original `Players_Score.csv`, or confirm that the release will use synthetic data only.
- [ ] Do not label reconstructed or synthetic data as the original paper dataset.
- [ ] Run `pytest -q` successfully.
- [ ] Run the paper-style experiment workflow with PuLP.
- [ ] Review generated teams, summaries and metadata files.
- [ ] Confirm that no local paths, private data or credentials are committed.

## Documentation

- [ ] Confirm the paper title, author names, journal citation and DOI.
- [ ] Review `CITATION.cff` and `.zenodo.json`.
- [ ] Update the changelog with the release date.
- [ ] Confirm the README commands work from a fresh environment.
- [ ] State clearly whether exact paper-result reproduction is possible.

## GitHub release

1. Open the repository's Releases page.
2. Choose **Draft a new release**.
3. Create the tag `v1.0.0` from `main`.
4. Use the title `v1.0.0 — Reproducible research implementation`.
5. Summarise the reusable optimiser, PuLP support, tests, experiment runner, citation metadata and data limitations.
6. Publish the release only after the CI workflow passes.

## Zenodo archive

1. Sign in to Zenodo using GitHub.
2. Enable this repository under GitHub integration.
3. Publish the GitHub release.
4. Verify the imported metadata, authors, licence and related paper DOI.
5. Publish the Zenodo record.
6. Add the resulting software DOI badge and citation to the README and `CITATION.cff`.

Zenodo creates the DOI only after its integration processes a published GitHub release. The DOI must not be invented or added in advance.
