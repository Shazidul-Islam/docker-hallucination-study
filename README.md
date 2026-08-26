# docker-hallucination-study

# LLM-Hallucinated Docker Image Recommendations

Automated pipeline for measuring Docker image hallucination in LLM-generated
Dockerfile `FROM` instructions. Derives scenarios from the Henkel et al. Dataset
of Dockerfiles, collects responses from 5 LLMs, and validates them against the
Docker Hub and endoflife.date APIs.

Run `docker_pipeline_full_automation.ipynb` in Google Colab.
