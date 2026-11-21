# LLM-Hallucinated Docker Image Recommendations — Replication Package

Code and data for the paper *"LLM-Hallucinated Docker Image Recommendations as a Container Supply-Chain Risk"*.
The package contains every script, raw LLM response and validation result used for the numbers, tables and
figures in the paper, including the robustness checks and the repair study added in the revision.

## Repository layout

```
notebooks/
  01_main_pipeline.ipynb                  scenario derivation, LLM collection, validation, classification
  02_recheck_and_supplementary_checks.ipynb  re-check of failed lookups, other registries, namespaces,
                                          Trivy CVE scan, hadolint baseline, knowledge-cutoff placement
  03_robustness_and_repair_runs.ipynb     repeated runs, temperature 0, web vs. API, image-free prompts,
                                          repair study (LLM API calls)
analysis/                                 offline scripts that reproduce every reported number from data/
data/
  phase1_original/                        manual labels of the 110 Phase 1 responses and the
                                          side-by-side comparison with the automated labels
  combined/                               all 370 responses: before and after the re-check
  supplementary/                          other registries, namespaces, maintenance, CVEs, hadolint flags
  robustness/                             repeated runs, web vs. API, image-free prompts (raw responses)
  repair/                                 repair study (raw responses and final outcomes)
figures/                                  Fig. 1–3 as used in the paper
```

## Where each result comes from

| Paper | Result | Data | Reproduce with |
|---|---|---|---|
| Table II, Sec. IV-A | 314 in-scope responses, category shares, "% resolved" | `data/combined/combined_full_results_rechecked.csv` | `analysis/overall_and_mainstream_niche.py` |
| Sec. III-D | 30 failed lookups re-checked and reclassified | `data/combined/recheck_30_rows.csv` | notebook 02, step 1 |
| Sec. III-D, Lim. (vi) | 81.8% agreement with the authors' manual labels | `data/phase1_original/` | `analysis/pipeline_vs_manual_labels.py` |
| Sec. IV-A | 56 references to other registries (25 do not resolve) | `data/supplementary/registry_check_56.csv` | notebook 02, step 2 |
| Fig. 2 | Per-LLM breakdown | `data/combined/combined_full_results_rechecked.csv` | `analysis/make_figures.py` |
| Fig. 3, Sec. IV-B | Mainstream vs. Niche, Fisher's exact tests, cutoff-adjusted Strict | same | `analysis/overall_and_mainstream_niche.py` |
| Table III, Sec. IV-C | Overlapping issues, hadolint 2.15.1 baseline | `data/supplementary/issue_flags_hadolint.csv` | notebook 02, step 5 |
| Sec. IV-C | Namespaces, repository maintenance, Trivy v0.76.2 CVEs | `data/supplementary/risk_*.csv`, `cve_*.csv` | notebook 02, steps 3–4 |
| Sec. IV-B, IV-F | Outdated Tags vs. documented knowledge cutoffs | `data/supplementary/issue_flags_hadolint.csv` | notebook 02, step 6 |
| Sec. IV-D | Repeated runs, Fleiss' κ, temperature 0 | `data/robustness/issue4_repeated_runs.csv` | `analysis/repeated_runs_and_temperature.py` |
| Sec. IV-D | Web vs. API, image-free prompts | `data/robustness/issue5*.csv` | `analysis/web_vs_api_and_image_free_prompts.py` |
| Table IV, Sec. IV-E | Repair study (79 attempts) | `data/repair/` | `analysis/repair_study.py` |
| Fig. 1 | Workflow diagram | — | `analysis/make_figures.py` |

## Quick start (no API keys needed)

```bash
pip install -r requirements.txt
python analysis/overall_and_mainstream_niche.py
python analysis/pipeline_vs_manual_labels.py
python analysis/repeated_runs_and_temperature.py
python analysis/web_vs_api_and_image_free_prompts.py
python analysis/repair_study.py
python analysis/make_figures.py
```

All scripts are run from the repository root and only read the files in `data/`.

## Re-running the data collection

The notebooks were run in Google Colab. API keys are read from Colab Secrets (`OPENAI_API_KEY`,
`ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `DEEPSEEK_API_KEY`, `GROQ_API_KEY`); no key is stored in this repository.
LLM outputs are not deterministic and Docker Hub, endoflife.date and CVE data change over time, so a new run
will not reproduce the exact responses. The files in `data/` are the snapshots used in the paper
(validation and re-checks: 20 Nov. 2026).

* Notebook 01 needs the base-image frequency table derived from the Henkel et al. Dataset of Dockerfiles
  (https://doi.org/10.5281/zenodo.3628771). Its Part 5 (12-row repair case study) is the preliminary study of
  the original submission and is superseded by notebook 03.
* Notebook 02 needs network access to Docker Hub and the other registries; step 4 pulls images for Trivy and
  takes several hours.
* Notebook 03 makes about 795 API calls. Gemini is disabled there because of its free-tier quota.

## Notes on the data

* Category names: `Nonexistent Tag`, `Non-Existent Image`, `Non-Official Image`, `Risky Latest Tag`,
  `Outdated Tag`, `Valid Official Image`, `NEEDS MANUAL CHECK` (Needs Manual Review in the paper) and
  `OUT OF SCOPE` (registries other than Docker Hub).
* `combined_final_report_before_recheck.xlsx` is the state before the 30 failed lookups were re-checked;
  `combined_full_results_rechecked.csv` is the state reported in the paper.
* In the repair study, 10 answers that wrapped the `FROM` line in Markdown or appended a digest were re-parsed
  by hand; the corrections are listed in `analysis/repair_study.py`.

## License

Code: MIT License. Data: CC BY 4.0.
