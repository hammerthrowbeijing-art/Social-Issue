from __future__ import annotations

import json
import math
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = Path(r"C:\Users\Larry.Nie\Downloads\B50_X_COMMENT.xlsx")
FIGURES_DIR = REPO_ROOT / "outputs" / "figures"
TABLES_DIR = REPO_ROOT / "outputs" / "tables"
DOCS_DIR = REPO_ROOT / "docs"

IV = "Author's attention quantity"
DV_COLUMNS = [
    "retweets count",
    "likes",
    "Comment word length",
    "Comment views",
    "followers",
]
CONTROL_COLUMNS = [
    "verified",
    "english",
    "log_media_outlets",
    "log_author_posts",
]


def ensure_dirs() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)


def resolve_data_path() -> Path:
    raw = os.environ.get("BREAK50_DATA_PATH")
    if raw:
        data_path = Path(raw)
    else:
        data_path = DEFAULT_DATA_PATH
    if not data_path.exists():
        raise FileNotFoundError(
            "Could not find the local dataset. Set BREAK50_DATA_PATH to the path of B50_X_COMMENT.xlsx."
        )
    return data_path


def load_and_prepare(data_path: Path) -> pd.DataFrame:
    df = pd.read_excel(data_path).copy()

    numeric_cols = [
        IV,
        "retweets count",
        "likes",
        "Comment word length",
        "Comment views",
        "followers",
        "number of media outlets",
        "number of author posts",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["verified"] = df["blue_verified"].astype(int)
    df["english"] = (df["Comment language"] == "en").astype(int)
    df["any_retweet"] = (df["retweets count"] > 0).astype(int)
    df["any_like"] = (df["likes"] > 0).astype(int)

    df["log_attention"] = np.log1p(df[IV])
    df["log_retweets"] = np.log1p(df["retweets count"])
    df["log_likes"] = np.log1p(df["likes"])
    df["log_views"] = np.log1p(df["Comment views"])
    df["log_followers"] = np.log1p(df["followers"])
    df["log_media_outlets"] = np.log1p(df["number of media outlets"])
    df["log_author_posts"] = np.log1p(df["number of author posts"])

    df["attention_quartile"] = pd.qcut(
        df[IV].rank(method="first"),
        4,
        labels=["Q1 Lowest", "Q2", "Q3", "Q4 Highest"],
    )
    return df


def fmt_value(value: object) -> str:
    if isinstance(value, (int, np.integer)):
        return f"{int(value):,}"
    if isinstance(value, (float, np.floating)):
        if math.isnan(float(value)):
            return ""
        if abs(float(value)) >= 1000:
            return f"{float(value):,.2f}"
        return f"{float(value):.3f}"
    if pd.isna(value):
        return ""
    return str(value)


def df_to_markdown(df: pd.DataFrame, index: bool = True) -> str:
    table = df.copy()
    if index:
        table = table.reset_index()
    headers = [str(col) for col in table.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in table.iterrows():
        values = [fmt_value(v) for v in row.tolist()]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown_table(df: pd.DataFrame, path: Path, index: bool = True) -> None:
    path.write_text(df_to_markdown(df, index=index) + "\n", encoding="utf-8")


def normal_p_value(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2))


def ols_hc1(y: np.ndarray, x: np.ndarray, names: list[str]) -> tuple[pd.DataFrame, dict[str, float]]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    keep = np.isfinite(y) & np.all(np.isfinite(x), axis=1)
    x = x[keep]
    y = y[keep]

    n, k = x.shape
    xtx = x.T @ x
    xtx_inv = np.linalg.inv(xtx)
    beta = xtx_inv @ (x.T @ y)
    residuals = y - x @ beta

    meat = np.zeros((k, k))
    for i in range(n):
        xi = x[i : i + 1].T
        meat += (residuals[i] ** 2) * (xi @ xi.T)
    robust_cov = (n / (n - k)) * (xtx_inv @ meat @ xtx_inv)
    robust_se = np.sqrt(np.diag(robust_cov))
    z_values = beta / robust_se
    p_values = np.array([normal_p_value(z) for z in z_values])
    ci_low = beta - 1.96 * robust_se
    ci_high = beta + 1.96 * robust_se

    rss = float(np.sum(residuals**2))
    tss = float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - rss / tss if tss else float("nan")

    results = pd.DataFrame(
        {
            "term": names,
            "coef": beta,
            "robust_se": robust_se,
            "z": z_values,
            "p_value": p_values,
            "ci_low": ci_low,
            "ci_high": ci_high,
        }
    )
    meta = {"n": float(n), "r2": float(r2)}
    return results, meta


def significance_label(p_value: float) -> str:
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return ""


def descriptive_outputs(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    sample_overview = pd.DataFrame(
        {
            "metric": [
                "Comments",
                "Unique usernames",
                "Unique comment IDs",
                "Unique source posts",
                "Date start",
                "Date end",
                "English-language comments",
                "Verified accounts",
                "Comments with zero retweets",
            ],
            "value": [
                len(df),
                df["username"].nunique(),
                df["contentsid"].nunique(),
                df["Blog ID"].nunique(),
                df["date"].min().strftime("%Y-%m-%d %H:%M:%S"),
                df["date"].max().strftime("%Y-%m-%d %H:%M:%S"),
                int(df["english"].sum()),
                int(df["verified"].sum()),
                int((df["retweets count"] == 0).sum()),
            ],
        }
    )

    stats_cols = [IV] + DV_COLUMNS + ["number of media outlets", "number of author posts"]
    stats = (
        df[stats_cols]
        .agg(["count", "mean", "std", "min", "median", "max"])
        .T.rename(columns={"std": "sd"})
    )
    return sample_overview, stats


def correlation_output(df: pd.DataFrame) -> pd.DataFrame:
    corr_cols = [IV] + DV_COLUMNS
    spearman = df[corr_cols].corr(method="spearman").loc[IV, DV_COLUMNS]
    pearson = df[corr_cols].corr(method="pearson").loc[IV, DV_COLUMNS]
    correlation_table = pd.DataFrame(
        {
            "dependent_variable": DV_COLUMNS,
            "spearman_rho": [spearman[col] for col in DV_COLUMNS],
            "pearson_r": [pearson[col] for col in DV_COLUMNS],
        }
    )
    return correlation_table


def regression_outputs(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    x_names = ["Intercept", "log_attention", "verified", "english", "log_media_outlets", "log_author_posts"]
    x = np.column_stack(
        [
            np.ones(len(df)),
            df["log_attention"],
            df["verified"],
            df["english"],
            df["log_media_outlets"],
            df["log_author_posts"],
        ]
    )

    outcome_map = {
        "Retweets count (log1p exploratory model)": "log_retweets",
        "Likes (log1p)": "log_likes",
        "Comment word length": "Comment word length",
        "Comment views (log1p)": "log_views",
        "Followers (log1p)": "log_followers",
    }

    all_rows = []
    summary_rows = []
    for label, column in outcome_map.items():
        fit_df, meta = ols_hc1(df[column].to_numpy(), x, x_names)
        fit_df.insert(0, "outcome", label)
        all_rows.append(fit_df)

        attention_row = fit_df.loc[fit_df["term"] == "log_attention"].iloc[0]
        summary_rows.append(
            {
                "outcome": label,
                "attention_coef": attention_row["coef"],
                "robust_se": attention_row["robust_se"],
                "ci_low": attention_row["ci_low"],
                "ci_high": attention_row["ci_high"],
                "p_value": attention_row["p_value"],
                "sig": significance_label(attention_row["p_value"]),
                "r2": meta["r2"],
                "n": int(meta["n"]),
            }
        )

    model_details = pd.concat(all_rows, ignore_index=True)
    model_summary = pd.DataFrame(summary_rows)
    return model_details, model_summary


def quartile_output(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("attention_quartile", observed=False).agg(
        attention_min=(IV, "min"),
        attention_median=(IV, "median"),
        attention_max=(IV, "max"),
        retweet_rate=("any_retweet", "mean"),
        mean_retweets=("retweets count", "mean"),
        median_likes=("likes", "median"),
        median_word_length=("Comment word length", "median"),
        median_views=("Comment views", "median"),
        median_followers=("followers", "median"),
    )
    return grouped.reset_index()


def create_correlation_figure(correlation_table: pd.DataFrame) -> None:
    ordered = correlation_table.sort_values("spearman_rho")
    colors = ["#b85c38" if value < 0 else "#2f6f8f" for value in ordered["spearman_rho"]]

    fig, ax = plt.subplots(figsize=(9.4, 5.6))
    bars = ax.barh(ordered["dependent_variable"], ordered["spearman_rho"], color=colors, edgecolor="#222222")
    ax.axvline(0, color="#444444", linewidth=1)
    ax.set_xlabel("Spearman correlation with author's attention quantity")
    ax.set_title("Break 50: Bivariate Associations with Author Attention Quantity")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar, value in zip(bars, ordered["spearman_rho"]):
        x = bar.get_width()
        ax.text(
            x + (0.012 if x >= 0 else -0.012),
            bar.get_y() + bar.get_height() / 2,
            f"{value:.3f}",
            va="center",
            ha="left" if x >= 0 else "right",
            fontsize=10,
        )

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "attention_correlations.png", dpi=220)
    plt.close(fig)


def create_quartile_figure(quartile_table: pd.DataFrame) -> None:
    labels = quartile_table["attention_quartile"].tolist()
    x = np.arange(len(labels))

    series = [
        ("retweet_rate", "Retweet rate", "#2f6f8f"),
        ("median_likes", "Median likes", "#508d4e"),
        ("median_word_length", "Median word length", "#9c6644"),
        ("median_views", "Median views", "#7b2cbf"),
        ("median_followers", "Median followers", "#d97706"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    axes = axes.flatten()
    for i, (column, title, color) in enumerate(series):
        ax = axes[i]
        values = quartile_table[column].to_numpy(dtype=float)
        ax.plot(x, values, marker="o", linewidth=2, color=color)
        ax.set_xticks(x, labels, rotation=20)
        ax.set_title(title)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        if column != "retweet_rate":
            ax.ticklabel_format(style="plain", axis="y")
    axes[-1].axis("off")
    fig.suptitle("Outcome Patterns Across Author Attention Quartiles", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(FIGURES_DIR / "attention_quartiles.png", dpi=220)
    plt.close(fig)


def create_coefficient_figure(model_summary: pd.DataFrame) -> None:
    ordered = model_summary.iloc[::-1].copy()

    fig, ax = plt.subplots(figsize=(9.4, 5.8))
    y = np.arange(len(ordered))
    x = ordered["attention_coef"].to_numpy(dtype=float)
    xerr = np.vstack(
        [
            x - ordered["ci_low"].to_numpy(dtype=float),
            ordered["ci_high"].to_numpy(dtype=float) - x,
        ]
    )

    ax.errorbar(x, y, xerr=xerr, fmt="o", color="#1f2937", ecolor="#1f2937", capsize=4)
    ax.axvline(0, color="#666666", linewidth=1)
    ax.set_yticks(y, ordered["outcome"])
    ax.set_xlabel("Coefficient for log(author's attention quantity)")
    ax.set_title("Controlled OLS Estimates for Author Attention Quantity")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for idx, row in ordered.reset_index(drop=True).iterrows():
        ax.text(
            row["ci_high"] + 0.02,
            idx,
            f"p={row['p_value']:.3f}" if row["p_value"] >= 0.001 else "p<0.001",
            va="center",
            fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "attention_coefficients.png", dpi=220)
    plt.close(fig)


def build_report(
    data_path: Path,
    df: pd.DataFrame,
    sample_overview: pd.DataFrame,
    descriptive_stats: pd.DataFrame,
    correlation_table: pd.DataFrame,
    model_summary: pd.DataFrame,
    quartile_table: pd.DataFrame,
) -> None:
    date_start = df["date"].min().strftime("%B %d, %Y")
    date_end = df["date"].max().strftime("%B %d, %Y")
    english_share = df["english"].mean()
    zero_retweet_share = (df["retweets count"] == 0).mean()

    strongest = correlation_table.sort_values("spearman_rho", ascending=False).iloc[0]
    weakest = correlation_table.sort_values("spearman_rho").iloc[0]
    likes_row = model_summary.loc[model_summary["outcome"] == "Likes (log1p)"].iloc[0]
    views_row = model_summary.loc[model_summary["outcome"] == "Comment views (log1p)"].iloc[0]
    followers_row = model_summary.loc[model_summary["outcome"] == "Followers (log1p)"].iloc[0]
    word_row = model_summary.loc[model_summary["outcome"] == "Comment word length"].iloc[0]
    retweet_row = model_summary.loc[
        model_summary["outcome"] == "Retweets count (log1p exploratory model)"
    ].iloc[0]

    report = f"""# Break 50 Analysis Report

## Overview

This report provides a repo-ready analysis output for the Break 50 project described in [`P3_plan.md`](./P3_plan.md). The analysis uses the local file `B50_X_COMMENT.xlsx` but does not copy the raw dataset into the repository, in keeping with the course instruction not to upload Excel or CSV data files to GitHub.

The project asks how **author's attention quantity** is related to five dependent variables:

- `retweets count`
- `likes`
- `Comment word length`
- `Comment views`
- `followers`

## Data And Sample

The working dataset contains **{len(df):,} comments** collected from **{date_start}** to **{date_end}**. The sample spans **{df["Blog ID"].nunique()} source posts**, **{df["username"].nunique():,} unique usernames**, and **{df["contentsid"].nunique():,} unique comment IDs**. About **{english_share:.1%}** of the comments are coded as English-language, and **{zero_retweet_share:.1%}** of the comments have zero retweets, which is why retweets are treated cautiously in the analysis.

Data source used locally: `{data_path}`

### Sample Overview

{df_to_markdown(sample_overview, index=False)}

### Descriptive Statistics

{df_to_markdown(descriptive_stats)}

## Analysis Strategy

The analysis follows the project plan and uses three layers of evidence:

1. Descriptive statistics for the independent variable, dependent variables, and control variables.
2. Bivariate correlations between author's attention quantity and each dependent variable.
3. Controlled OLS models using `log(1 + author's attention quantity)` as the focal predictor and the following controls: verified status, English-language indicator, `log(1 + number of media outlets)`, and `log(1 + number of author posts)`.

For `likes`, `Comment views`, and `followers`, the outcome is also log-transformed with `log(1 + y)`. `Comment word length` is kept on its original scale. `retweets count` is modeled with `log(1 + retweets)` as an exploratory approximation only; because retweets are highly zero-inflated, a negative binomial or hurdle model would be preferable in the final paper if additional packages are available.

## Bivariate Results

The strongest raw association is between author's attention quantity and **{strongest["dependent_variable"]}** (`Spearman rho = {strongest["spearman_rho"]:.3f}`). The weakest relationship is **{weakest["dependent_variable"]}** (`Spearman rho = {weakest["spearman_rho"]:.3f}`).

### Correlation Table

{df_to_markdown(correlation_table, index=False)}

![Correlation plot](../outputs/figures/attention_correlations.png)

## Controlled Model Results

The controlled models show a consistent pattern:

- Higher author's attention quantity is associated with more likes (`b = {likes_row["attention_coef"]:.3f}`, `p {"<0.001" if likes_row["p_value"] < 0.001 else f"= {likes_row['p_value']:.3f}"}`).
- Higher author's attention quantity is associated with more comment views (`b = {views_row["attention_coef"]:.3f}`, `p {"<0.001" if views_row["p_value"] < 0.001 else f"= {views_row['p_value']:.3f}"}`).
- The strongest positive relationship is with followers (`b = {followers_row["attention_coef"]:.3f}`, `p {"<0.001" if followers_row["p_value"] < 0.001 else f"= {followers_row['p_value']:.3f}"}`).
- Comment word length is modestly negative (`b = {word_row["attention_coef"]:.3f}`, `p {"<0.001" if word_row["p_value"] < 0.001 else f"= {word_row['p_value']:.3f}"}`), suggesting that higher-attention authors do not necessarily write longer comments.
- The retweet model is weak and not statistically reliable in this specification (`b = {retweet_row["attention_coef"]:.3f}`, `p {"<0.001" if retweet_row["p_value"] < 0.001 else f"= {retweet_row['p_value']:.3f}"}`).

### Model Summary

{df_to_markdown(model_summary, index=False)}

![Coefficient plot](../outputs/figures/attention_coefficients.png)

## Quartile Check

To make the pattern easier to interpret substantively, the comments were also grouped into four quartiles of author's attention quantity. The quartile summary shows that the highest-attention quartile has notably higher median views and median followers than the lower quartiles, while the retweet pattern is much noisier.

### Quartile Summary

{df_to_markdown(quartile_table, index=False)}

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
$env:BREAK50_DATA_PATH=\"{data_path}\"
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
"""
    (DOCS_DIR / "analysis_report.md").write_text(report, encoding="utf-8")


def write_json_summary(
    data_path: Path,
    df: pd.DataFrame,
    correlation_table: pd.DataFrame,
    model_summary: pd.DataFrame,
) -> None:
    payload = {
        "data_path": str(data_path),
        "n_comments": int(len(df)),
        "date_start": df["date"].min().strftime("%Y-%m-%d %H:%M:%S"),
        "date_end": df["date"].max().strftime("%Y-%m-%d %H:%M:%S"),
        "strongest_spearman_outcome": correlation_table.sort_values("spearman_rho", ascending=False)
        .iloc[0]["dependent_variable"],
        "model_summary": model_summary.to_dict(orient="records"),
    }
    (TABLES_DIR / "analysis_summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    data_path = resolve_data_path()
    df = load_and_prepare(data_path)

    sample_overview, descriptive_stats = descriptive_outputs(df)
    correlation_table = correlation_output(df)
    model_details, model_summary = regression_outputs(df)
    quartile_table = quartile_output(df)

    write_markdown_table(sample_overview, TABLES_DIR / "sample_overview.md", index=False)
    write_markdown_table(descriptive_stats, TABLES_DIR / "descriptive_stats.md", index=True)
    write_markdown_table(correlation_table, TABLES_DIR / "correlations.md", index=False)
    write_markdown_table(model_summary, TABLES_DIR / "model_summary.md", index=False)
    write_markdown_table(model_details, TABLES_DIR / "model_details.md", index=False)
    write_markdown_table(quartile_table, TABLES_DIR / "quartile_summary.md", index=False)

    create_correlation_figure(correlation_table)
    create_quartile_figure(quartile_table)
    create_coefficient_figure(model_summary)
    build_report(
        data_path,
        df,
        sample_overview,
        descriptive_stats,
        correlation_table,
        model_summary,
        quartile_table,
    )
    write_json_summary(data_path, df, correlation_table, model_summary)

    print(f"Analysis complete. Report written to: {DOCS_DIR / 'analysis_report.md'}")


if __name__ == "__main__":
    main()
