
# Week 2 Assignment – Testing Mindset

## Overview

This project evaluates the reliability and reproducibility of a differential expression analysis using simulated RNA-seq data and DESeq2.

The dataset will contain 1,000 simulated genes from six samples (3 control and 3 treatment). A known treatment effect will be introduced in 50 genes, allowing the results of the analysis to be compared with a known biological signal.

### Research Question

**Can a DESeq2 differential expression workflow reliably recover known treatment effects from simulated RNA-seq data?**

### Why this analysis?

My research involves sequencing data and differential expression analysis, but
I have not previously used simulated RNA-seq data to systematically test an
analysis pipeline using known-answer, negative-control, positive-control,
invariant, redundancy, and determinism checks.

### Workflow

```text
Simulate RNA-seq count data
        |
Introduce known treatment effects
        |
Run differential expression analysis with DESeq2
        |
Identify differentially expressed genes
        |
Compare results with the known simulated signal
        |
Apply controls and reproducibility checks
```

## Testing and Controls

### 1. Known Answer

Because the data are simulated, the genes with true differential expression are known before running DESeq2.

The analysis will compare the genes detected by DESeq2 with the 50 genes simulated to have a treatment effect. This will allow us to determine how many true effects were successfully recovered and whether genes without a simulated effect were incorrectly identified.

### 2. Invariant

Changing the order of the samples should not change the results as long as the count matrix and sample metadata remain correctly matched.

The samples will be reordered and the differential expression analysis repeated. The results will then be compared with the original analysis to confirm that the results are unchanged.

### 3. Negative Control

The treatment signal will be intentionally destroyed by randomly permuting the control and treatment labels while keeping the count data unchanged.

This preserves the expression values and characteristics of each sample but destroys the relationship between gene expression and treatment.

The permutation will be repeated multiple times, and the number of significant genes from each analysis will be used to generate a null distribution. The original result will then be compared with this distribution.

### 4. Positive Control

Known treatment effects will be intentionally introduced into the simulated data.

Different effect sizes will be tested to determine whether DESeq2 can detect the planted signal and how detection changes as the signal becomes weaker.

For example, effects ranging from strong to weak can be simulated to identify the level at which the workflow no longer consistently detects differential expression.

### 5. Redundancy

The treatment effect will be estimated in two ways.

First, DESeq2 will be used to calculate the log2 fold change for each gene. Second, fold changes will be calculated directly from expression summaries for the control and treatment groups.

The direction and magnitude of the estimates will be compared.

Both approaches use the same underlying data and treatment groups, so errors in the input data or sample labels could affect both methods.

### 6. Order of Magnitude

Expected results will be recorded before running the analysis.

Because 50 genes are simulated with a true treatment effect, the expected number of true discoveries should be on the order of tens rather than hundreds. The negative control is expected to produce substantially fewer significant genes.

The observed results will be compared with these expectations to identify potentially implausible outcomes.

### 7. Determinism

The analysis will be repeated to determine whether the same inputs produce the same outputs.

A fixed random seed will be used for simulation and permutation steps:

```r
set.seed(123)
```

The complete analysis will be run more than once using the same settings. If possible, it will also be run in another computational environment or by another person.

## Data Provenance

All RNA-seq count data used in this project are simulated directly in R. The complete data-generation procedure and random seed will be included in the analysis so that the dataset can be recreated.

## Computational Environment

The analysis will be performed in R using DESeq2 and documented in R Markdown.

Software and package versions will be recorded using:

```r
sessionInfo()
```

The complete analysis and its development history will be maintained in the GitHub repository.

## GitHub Repository

(**Repository:**) [https://github.com/Matioli-amoc/BIOL7800.git]
