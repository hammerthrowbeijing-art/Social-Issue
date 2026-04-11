# Break 50 Analysis Report

## Overview

This report provides a repo-ready analysis output for the Break 50 project described in [`P3_plan.md`](./P3_plan.md). The analysis uses the local file `B50_X_COMMENT.xlsx` but does not copy the raw dataset into the repository, in keeping with the course instruction not to upload Excel or CSV data files to GitHub.

The project asks how **author's attention quantity** is related to five dependent variables:

- `retweets count`
- `likes`
- `Comment word length`
- `Comment views`
- `followers`

## Data And Sample

The working dataset contains **1,008 comments** collected from **July 23, 2024** to **August 01, 2024**. The sample spans **4 source posts**, **740 unique usernames**, and **845 unique comment IDs**. About **91.3%** of the comments are coded as English-language, and **90.1%** of the comments have zero retweets, which is why retweets are treated cautiously in the analysis.

Data source used locally: `C:\Users\Larry.Nie\Downloads\B50_X_COMMENT.xlsx`

### Sample Overview

| metric | value |
| --- | --- |
| Comments | 1,008 |
| Unique usernames | 740 |
| Unique comment IDs | 845 |
| Unique source posts | 4 |
| Date start | 2024-07-23 02:02:13 |
| Date end | 2024-08-01 02:43:46 |
| English-language comments | 920 |
| Verified accounts | 833 |
| Comments with zero retweets | 908 |

### Descriptive Statistics

| index | count | mean | sd | min | median | max |
| --- | --- | --- | --- | --- | --- | --- |
| Author's attention quantity | 1,008.00 | 2,416.94 | 9,841.60 | 0.000 | 605.000 | 165,946.00 |
| retweets count | 1,008.00 | 0.342 | 2.028 | 0.000 | 0.000 | 32.000 |
| likes | 1,008.00 | 32.669 | 212.513 | 0.000 | 1.000 | 5,174.00 |
| Comment word length | 1,008.00 | 12.563 | 10.549 | 1.000 | 10.000 | 59.000 |
| Comment views | 1,008.00 | 6,952.46 | 28,414.98 | 1.000 | 290.000 | 456,687.00 |
| followers | 1,008.00 | 13,940.37 | 105,949.52 | 2.000 | 756.000 | 2,889,009.00 |
| number of media outlets | 1,008.00 | 1,816.96 | 4,437.72 | 0.000 | 435.500 | 80,628.00 |
| number of author posts | 1,008.00 | 22,199.89 | 48,105.28 | 25.000 | 7,871.50 | 528,173.00 |

## Analysis Strategy

The analysis follows the project plan and uses three layers of evidence:

1. Descriptive statistics for the independent variable, dependent variables, and control variables.
2. Bivariate correlations between author's attention quantity and each dependent variable.
3. Controlled OLS models using `log(1 + author's attention quantity)` as the focal predictor and the following controls: verified status, English-language indicator, `log(1 + number of media outlets)`, and `log(1 + number of author posts)`.

For `likes`, `Comment views`, and `followers`, the outcome is also log-transformed with `log(1 + y)`. `Comment word length` is kept on its original scale. `retweets count` is modeled with `log(1 + retweets)` as an exploratory approximation only; because retweets are highly zero-inflated, a negative binomial or hurdle model would be preferable in the final paper if additional packages are available.

## Bivariate Results

The strongest raw association is between author's attention quantity and **followers** (`Spearman rho = 0.675`). The weakest relationship is **Comment word length** (`Spearman rho = -0.084`).

### Correlation Table

| dependent_variable | spearman_rho | pearson_r |
| --- | --- | --- |
| retweets count | 0.085 | 0.037 |
| likes | 0.171 | 0.083 |
| Comment word length | -0.084 | 0.080 |
| Comment views | 0.234 | 0.082 |
| followers | 0.675 | 0.177 |

![Correlation plot](../outputs/figures/attention_correlations.png)

## Controlled Model Results

The controlled models show a consistent pattern:

- Higher author's attention quantity is associated with more likes (`b = 0.134`, `p = 0.001`).
- Higher author's attention quantity is associated with more comment views (`b = 0.231`, `p <0.001`).
- The strongest positive relationship is with followers (`b = 0.452`, `p <0.001`).
- Comment word length is modestly negative (`b = -0.626`, `p = 0.036`), suggesting that higher-attention authors do not necessarily write longer comments.
- The retweet model is weak and not statistically reliable in this specification (`b = 0.012`, `p = 0.353`).

### Model Summary

| outcome | attention_coef | robust_se | ci_low | ci_high | p_value | sig | r2 | n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Retweets count (log1p exploratory model) | 0.012 | 0.013 | -0.013 | 0.036 | 0.353 |  | 0.025 | 1,008 |
| Likes (log1p) | 0.134 | 0.042 | 0.053 | 0.215 | 0.001 | ** | 0.082 | 1,008 |
| Comment word length | -0.626 | 0.299 | -1.211 | -0.040 | 0.036 | * | 0.096 | 1,008 |
| Comment views (log1p) | 0.231 | 0.063 | 0.109 | 0.354 | 0.000 | *** | 0.115 | 1,008 |
| Followers (log1p) | 0.452 | 0.032 | 0.388 | 0.515 | 0.000 | *** | 0.601 | 1,008 |

![Coefficient plot](../outputs/figures/attention_coefficients.png)

## Quartile Check

To make the pattern easier to interpret substantively, the comments were also grouped into four quartiles of author's attention quantity. The quartile summary shows that the highest-attention quartile has notably higher median views and median followers than the lower quartiles, while the retweet pattern is much noisier.

### Quartile Summary

| attention_quartile | attention_min | attention_median | attention_max | retweet_rate | mean_retweets | median_likes | median_word_length | median_views | median_followers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 Lowest | 0 | 160.500 | 283 | 0.079 | 0.440 | 1.000 | 11.000 | 140.500 | 235.000 |
| Q2 | 283 | 425.000 | 604 | 0.095 | 0.234 | 2.000 | 10.000 | 233.000 | 441.000 |
| Q3 | 606 | 897.000 | 1,648 | 0.071 | 0.147 | 2.000 | 8.500 | 448.000 | 894.000 |
| Q4 Highest | 1,648 | 3,771.50 | 165,946 | 0.151 | 0.548 | 2.000 | 9.500 | 654.000 | 3,969.00 |

![Quartile plot](../outputs/figures/attention_quartiles.png)

## Interpretation

Overall, the findings support the central claim of the project plan: **author's attention quantity is positively associated with visibility-oriented and reach-oriented outcomes**, especially followers, comment views, and likes. The relationship with retweets is much weaker, and the relationship with comment word length is slightly negative. In practical terms, this means that authors with higher attention quantity appear to occupy more advantaged audience positions and receive more visible engagement, but they do not necessarily produce longer comments or more shareable comments.

## Limitations

- The analysis uses one Break 50 dataset collected over a short time window, so external validity is limited.
- The data are observational, so the models identify association rather than causation.
- Retweets are highly zero-inflated, so the retweet model should be treated as exploratory.
- The classical count-model approach proposed in the plan was approximated here with available local packages; the final project can strengthen this step by switching to a negative binomial or hurdle model if `statsmodels` becomes available.

## Reproduction

From the repository root, run:

```powershell
$env:BREAK50_DATA_PATH="C:\Users\Larry.Nie\Downloads\B50_X_COMMENT.xlsx"
py -X utf8 scripts/run_analysis.py
```

Generated outputs:

- [`../outputs/figures/attention_correlations.png`](../outputs/figures/attention_correlations.png)
- [`../outputs/figures/attention_coefficients.png`](../outputs/figures/attention_coefficients.png)
- [`../outputs/figures/attention_quartiles.png`](../outputs/figures/attention_quartiles.png)
- [`../outputs/tables/sample_overview.md`](../outputs/tables/sample_overview.md)
- [`../outputs/tables/descriptive_stats.md`](../outputs/tables/descriptive_stats.md)
- [`../outputs/tables/correlations.md`](../outputs/tables/correlations.md)
- [`../outputs/tables/model_summary.md`](../outputs/tables/model_summary.md)
- [`../outputs/tables/model_details.md`](../outputs/tables/model_details.md)
- [`../outputs/tables/quartile_summary.md`](../outputs/tables/quartile_summary.md)
