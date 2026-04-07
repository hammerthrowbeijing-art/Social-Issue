## 1. Research Questions & Significance

For each research question, address all three components below. The goal is to show the logical connection between the phenomenon under investigation, the question being asked, and why it matters.

### RQ 1

The Question: This project asks how author's attention quantity is related to comment-level outcomes in the Break 50 discussion dataset, with specific attention to retweets count, likes, comment word length, comment views, and followers. In this design, author's attention quantity is the focal independent variable, while the five listed indicators serve as the dependent variables that capture amplification, appreciation, visibility, textual expression, and audience reach.

The Context: What phenomenon, debate, or gap does this question address?

This question addresses a broader communication and platform-studies debate about how attention structures shape visibility in digital discourse. Much of the existing conversation about social media influence centers on likes, follower counts, or the popularity of posts themselves, but less attention is given to whether an author's own attention behavior is associated with how their comments circulate and what kind of audience position they occupy. The Break 50 dataset provides a bounded case within sports-media discourse, allowing the study to examine whether more attention-intensive authors tend to receive stronger engagement, broader exposure, or different patterns of comment expression inside a single project-specific conversation.

Why It Matters: Who cares about this question? Why now? What's at stake for stakeholders (e.g., athletes, fans, media, organizations, policymakers, researchers)?

This question matters to several groups. For sports-media producers and creator teams, it can clarify which types of participant accounts are most likely to generate visible interaction around Break 50 content. For communication researchers, it offers a way to connect micro-level commenting behavior to larger theories of attention, influence, and platform visibility. For audiences and public-discourse scholars, it matters because social media conversations are not neutral spaces; some voices receive more exposure than others, and understanding the role of author-level attention characteristics helps explain why certain comments travel further, gather more endorsement, or appear more prominent within a public event-driven discussion.


## 2. Dataset Selection & Justification

Identify which dataset you are using and explain why.

Dataset Choice: Break 50 X/Twitter comment dataset

Justification: This project will use only the Break 50 comment dataset stored in B50_X_COMMENT.xlsx. The file contains 1,008 public comments collected between July 23, 2024 and August 01, 2024, drawn from 4 Break 50-related posts and representing 740 unique usernames and 845 unique comment IDs. It is an appropriate dataset because it includes the focal independent variable (Author's attention quantity) and all five dependent variables needed for the project (retweets count, likes, Comment word length, Comment views, and followers), along with auxiliary fields such as language, verification status, posting activity, and date. Using one internally consistent dataset keeps the measurement framework coherent and ensures that all variables are observed at the same platform level and within the same event-centered conversation. The dataset is also analytically useful because it is mostly English-language (920 comments, 91.3%) and contains no missing values in the core variables, which supports a cleaner comment-level design.

Key files you plan to use: B50_X_COMMENT.xlsx


## 3. Preliminary Variable Operationalization

For your main constructs, describe how you will measure or identify them in the data.


| Construct | Operational Definition | Data Source / Indicator |
| --- | --- | --- |
| Independent variable: author attention quantity | The author's attention quantity will be measured using the spreadsheet field Author's attention quantity. Because the distribution is highly right-skewed, both the raw value and a log(1+x) transformed version will be considered. | B50_X_COMMENT.xlsx: Author's attention quantity |
| Dependent variable: comment amplification | Amplification will be measured by retweets count, interpreted as the degree to which a comment is redistributed by other users. This variable is heavily zero-inflated and will likely require a count-based model. | B50_X_COMMENT.xlsx: retweets count |
| Dependent variable: comment appreciation | Appreciation will be measured by likes, indicating visible endorsement or positive reaction to a comment. Due to skew, the main model will use a log(1+x) transformation. | B50_X_COMMENT.xlsx: likes |
| Dependent variable: textual expression | Textual expression will be measured by Comment word length, used as a proxy for how brief or elaborate a comment is. | B50_X_COMMENT.xlsx: Comment word length |
| Dependent variable: comment visibility | Visibility will be measured by Comment views, reflecting how broadly a comment was exposed on the platform. This variable will also be evaluated on a log(1+x) scale. | B50_X_COMMENT.xlsx: Comment views |
| Dependent variable: author audience reach | Audience reach will be measured by followers. This is an author-level outcome and will be interpreted cautiously as the type of audience position associated with higher attention quantity rather than as an immediate reaction to a single comment. | B50_X_COMMENT.xlsx: followers |
| Potential controls | To reduce omitted-variable bias, the analysis may include control variables for verification status, number of media outlets, number of author posts, comment language, and date or posting period. | B50_X_COMMENT.xlsx: blue_verified, number of media outlets, number of author posts, Comment language, date |


## 4. Proposed Analyses

Outline the analytical approaches you plan to use. For each, explain how it addresses your RQ.

| Analysis Type | Description | RQ Addressed |
| --- | --- | --- |
| Descriptive profiling | Summarize the distributions, central tendencies, outliers, and missingness of all focal variables. This step will justify transformations and highlight that retweets are especially sparse (908 of 1,008 comments have zero retweets). | RQ 1 |
| Bivariate rank-order analysis | Estimate Spearman correlations between author's attention quantity and each dependent variable. This is an appropriate exploratory step because the variables are measured on very different scales and several are strongly skewed. | RQ 1 |
| Count model for retweets | Model retweets count using a negative binomial, hurdle, or other zero-aware count specification, with author's attention quantity as the key predictor and auxiliary controls added as needed. | RQ 1 |
| Log-linear models for likes, views, and followers | Estimate separate regressions for log(1+likes), log(1+Comment views), and log(1+followers) as a function of log(1+author's attention quantity), with robust standard errors and optional controls. | RQ 1 |
| Linear model for word length | Estimate whether author's attention quantity predicts Comment word length. Because word length is a content-feature outcome rather than an engagement count, it will be analyzed separately from the amplification metrics. | RQ 1 |
| Sensitivity checks | Compare results with and without controls, assess whether English-only comments change the results, and test whether conclusions are driven by extreme high-visibility accounts. | RQ 1 |


## 5. Limitations & Potential Issues

Identify at least 2-3 limitations or challenges with your approach. Be honest; acknowledging limits is a strength, not a weakness.

- The study is limited to a single Break 50 dataset collected over a short period, so the findings may reflect the dynamics of this specific project and time window rather than general patterns across other sports-media conversations or platforms.

- The data are observational rather than experimental, so the analysis can identify association but cannot establish that higher author's attention quantity causes stronger engagement or visibility. Other unmeasured factors, such as account reputation, offline fame, or the substance of the comment, may shape the observed relationships.

- Several dependent variables are highly skewed, and retweets count is especially zero-heavy. This creates a risk that simple linear models would be misleading unless transformations or count-based specifications are used.

- One dependent variable, followers, is conceptually different from the others because it is an author-level audience attribute rather than a direct reaction to an individual comment. Its interpretation therefore requires caution and should be framed as a structural association, not an immediate comment effect.


## 6. Ethical Considerations

Address the following: Privacy, harm, and bias. Consider whether the data are public or private, whether the analysis could identify individuals, and whether the study could reinforce problematic assumptions.

This study uses public social media data, so privacy risk is lower than in studies based on private messages or restricted user records. Even so, ethical reporting still matters: individual usernames should not be highlighted unnecessarily, quoted comments should be used sparingly, and results should be reported in aggregate whenever possible. The analysis could also introduce harm if highly visible comments are treated as a proxy for comment quality or if politically charged or emotionally polarizing remarks are amplified without context. Bias may enter through platform algorithms, verification advantages, language distribution, and the fact that the dataset captures only those comments that were available in this collection window. For these reasons, the project should interpret the results as platform-conditioned patterns rather than as neutral or universal measures of social value.


## 7. Group Role Assignments

Specify who is responsible for what. Titles are flexible, but responsibilities must be clear.

| Role | Group Member | Primary Responsibilities |
| --- | --- | --- |
| Project & Data Lead | Larry Nie | Dataset inspection, variable selection, data-quality review, and final file management. |
| Methods Lead | Larry Nie | Model selection, exploratory correlation analysis, robustness strategy, and interpretation of findings. |
| Writing & Visualization Lead | Larry Nie | Drafting the project plan, producing the figure, and aligning the final document with academic style requirements. |


## 8. Data Visualization Plan

Create at least ONE data visualization that addresses your research question(s). This is a required deliverable due with your project plan.

Primary Goal: What story does your visualization tell? What specific question does it answer?

The visualization is designed to compare the relative strength and direction of the association between author's attention quantity and each dependent variable. It answers the question of which outcomes are most closely aligned with higher author attention quantity in the Break 50 discussion.

Visualization Description: Describe what type of chart/graph you're creating and what it will show.

The figure is a horizontal bar chart showing the preliminary Spearman correlation between author's attention quantity and each of the five dependent variables: retweets count, likes, Comment word length, Comment views, and followers. Each bar reports the signed correlation coefficient, making it possible to compare outcomes on a common scale even though the original variables are measured very differently.

Design Rationale: Why did you choose this visualization type? How does it clarify your argument or make your data more understandable?

This visualization is appropriate because the variables are highly skewed and have different units, which makes raw-value comparisons difficult. A correlation bar chart provides a clean overview of relative association strength and direction without implying that the relationships are already causal or fully modeled. For a project-plan stage, this design is useful because it gives a concise preview of which outcomes appear most responsive to author attention quantity and where more careful modeling is still needed.

Verification Methods: How will you ensure your visualization accurately represents your data? - [√] Spot-checked calculations against source data - [ ] Had groupmate review for accuracy - [√] Verified variable labels and coefficient signs against the spreadsheet - [√] Recomputed the correlations using cleaned numeric columns

The Visualization: Embed your visualization here (as an image) or provide a link to the file.

![Break 50 correlation](break50_attention_correlation.png)


Brief Interpretation (2-3 sentences): What does this visualization show? What pattern or insight does it reveal?

The visualization suggests that author's attention quantity is most strongly associated with followers (Spearman rho = 0.675), followed by Comment views (rho = 0.234) and likes (rho = 0.171). Retweets count shows only a weak positive relationship (rho = 0.085), while Comment word length is weakly negative (rho = -0.084), implying that higher attention quantity may be more closely tied to audience reach and exposure than to longer textual expression.


## 9. AI-Assisted Work Documentation & Verification

If you used AI tools for any part of this plan, document your process and verification methods.

Tools Used: Which AI tools/IDEs did you use, and for what purpose?

Codex (a GPT-based coding assistant) was used to inspect the template document, profile the Break 50 dataset, generate the preliminary correlation visualization, and help draft the research-plan language in a more formal academic style.

Verification Methods: How did you verify AI outputs were accurate and appropriate?

- Code Explanation:

- [√] I reviewed the code logic used to read the spreadsheet, identify the focal variables, and compute the preliminary statistics

- [√] I reviewed the reasoning behind the chosen variable definitions, transformations, and visualization design

- [ ] N/A (didn't use code-generating AI)

- Output Validation:

- [√] I cross-checked row counts, date range, and variable names against the source file

- [√] I verified outputs make logical sense given my data

- [√] I compared AI-generated summaries with the observed distributions in the dataset

- Iterative Refinement:

- Number of prompt iterations before getting usable output: 3

- Key refinements made: narrowed the project to one focal independent variable, specified five dependent variables, added distribution-sensitive modeling choices, and revised the prose into a more rigorous academic register.

Learning Reflection: Working with AI was useful for accelerating the structuring of the project and the first round of exploratory analysis, but it also reinforced that variable meaning, model choice, and interpretation still require careful human review. Examining the AI-supported outputs made it clearer that rigorous research writing depends not only on generating text quickly, but on checking that the analytical logic truly matches the dataset and the research question.
