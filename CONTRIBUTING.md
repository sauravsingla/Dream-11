# Contributing

Thank you for considering a contribution to this research-code repository.

## Useful contributions

Contributions are especially welcome when they improve reproducibility or make the paper easier to build upon, including:

- fixes to the optimisation formulation or input validation;
- support for additional clearly documented datasets;
- reproducible comparison baselines;
- tests covering constraints and solver behaviour;
- documentation and worked examples;
- adapters for updated fantasy-cricket rules.

## Before opening a pull request

1. Open an issue describing the research or engineering problem.
2. Keep the proposed change focused and avoid unrelated formatting changes.
3. Use only data that can legally be redistributed, and document its source and licence.
4. Clearly distinguish synthetic, reconstructed and original data.
5. Add or update tests for behavioural changes.
6. Run the test suite locally:

```bash
pip install -e ".[test]"
pytest
```

## Reproducibility expectations

For experimental contributions, include:

- the exact command used;
- input-data provenance;
- package and solver versions;
- random seeds where applicable;
- expected output files or summary metrics;
- a statement explaining whether the result reproduces the article or extends it.

Comparisons with other algorithms should use the same player pool, constraints, scoring rules and information cutoff. See `docs/research_reuse.md` for the recommended comparison protocol.

## Code style

- Prefer small, readable functions with explicit inputs and outputs.
- Keep the open-source PuLP path working unless a contribution specifically targets an optional solver.
- Do not commit credentials, commercial solver licences, generated environments or private datasets.
- Use descriptive commit messages written as completed actions, such as `Add validation for duplicate players`.

## Citation and attribution

Retain the project citation metadata and acknowledge external datasets, libraries and methods. Research that uses the formulation, implementation or experiment design should cite the associated paper as shown in `README.md` and `CITATION.cff`.

## Pull-request description

A good pull request explains:

- what changed;
- why the change is needed;
- how it was tested;
- any limitations or compatibility considerations;
- whether results differ from the published paper.