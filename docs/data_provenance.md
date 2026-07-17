# Data provenance and reconstruction

## Status of the original research data

The notebook used a local file named `Players_Score.csv`. That exact source file is not currently available in this repository, and no verified public copy has been identified.

The original paper describes a pool of India and England players, their Dream11 prices, player categories, and fantasy scores from ten previous matches. The executed notebook preserves some rows and outputs, but it does not expose enough information to recreate every value with certainty.

For that reason, this repository does **not** present the included example dataset as the dataset used in the paper.

## Dataset labels used in this repository

- `data/example_players.csv`: fictional, synthetic data used only to demonstrate and test the optimisation workflow.
- `data/paper_players_score.csv`: reserved filename for the original research dataset, should it be recovered and its provenance verified.
- `data/reconstructed_players.csv`: recommended filename for any future reconstruction assembled from public sources.

## Requirements for a reconstructed dataset

A reconstructed dataset must include a companion note recording:

1. the target fixture and date;
2. the ten historical matches used for each player;
3. the fantasy-scoring rules and source;
4. the date and source of each player's credit price;
5. all transformations or missing-value decisions;
6. the person and date responsible for the reconstruction.

A reconstruction must be labelled clearly in the CSV documentation and must not be described as the original paper data.

## Recommended provenance columns

A reconstruction may keep the model input columns unchanged and store provenance in a separate file, such as `data/reconstructed_players_sources.csv`, with fields including:

```text
Player Name
Target Match
Target Match Date
Historical Match Dates
Score Source
Price Source
Price Capture Date
Scoring Rules Version
Notes
```

## Recovery checklist for the original file

Search historical laptops, external drives, email attachments, cloud storage, Colab notebooks and backups for:

```text
Players_Score.csv
E:\MSBA\Players_Score.csv
Dream 11
Dream_11
Integer Optimisation
```

Before publishing a recovered file, verify that it matches the notebook's visible rows, player count, means, standard deviations and selected-team outputs. Also confirm that publication does not violate data-provider terms or licensing restrictions.
