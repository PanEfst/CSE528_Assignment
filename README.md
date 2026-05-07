**CSE528 — LLM-as-a-Judge Toxicity Moderation with Gemma**



This repository contains the implementation for the CSE528 Deep Learning II assignment: **LLM-as-a-Judge Toxicity Moderation with Gemma**.



The project implements a toxicity moderation system using a small generative language model as a judge. Instead of training a traditional discriminative classifier, the system uses a generative LLM to return a structured moderation decision in strict JSON format.



The system supports three output labels:



\- TOXIC

\- NON\_TOXIC

\- DEFER



The DEFER label is used when the system is uncertain and should abstain from making a final automatic moderation decision.



\---



**Model and Execution Environment**



The implementation uses:



\- Model: google/gemma-2-2b-it

\- Backend: Hugging Face Transformers

\- Quantization: 4-bit quantization using bitsandbytes

\- Recommended runtime: Google Colab with T4 GPU

\- Fine-tuning: No fine-tuning or model training is performed.



The model is used only for inference.



\---



**Dataset**



The project uses the **Civil Comments** dataset.



The dataset is used only for:



\- evaluation

\- threshold selection

\- DEFER policy analysis

\- robustness testing



The notebook creates a balanced subset and saves the generated dataset files under:



data/splits/





The main saved files are:



civil\_comments\_5k\_sample.csv

validation.csv

test.csv

dataset\_stats.txt



\---



**Implemented Decision Mechanisms**



Three decision mechanisms are implemented and compared.



**A. Direct Generation**



The model receives a moderation prompt and directly generates a strict JSON object.



The output contains:



\- label

\- category

\- confidence

\- short rationale



**B. Log-likelihood Scoring**



The model scores three possible completions:



\- A = TOXIC

\- B= NON\_TOXIC

\- C = DEFER



The final label is selected based on the highest normalized score.





**C. Self-Consistency**



The model generates multiple sampled outputs. The final decision is based on majority vote.



If the vote agreement is low, the system returns DEFER.



\---



**Strict JSON Output**



The expected JSON schema is:



{

&#x20; "label": "TOXIC | NON\_TOXIC | DEFER",

&#x20; "category": "insult | threat | hate | harassment | profanity | other | none",

&#x20; "confidence": 0.0,

&#x20; "short\_rationale": "1-2 sentences max"

}



A JSON validator is implemented.



If the model output is invalid or incomplete, the system attempts to repair it. If repair is not possible, the system falls back to DEFER.



The implementation also reports the JSON validity rate.



\---



**Uncertainty and DEFER Policy**



The system supports abstention through the DEFER label.



DEFER can be triggered by:



\- low confidence

\- low log-likelihood separation

\- low self-consistency vote agreement

\- invalid or unrecoverable JSON output



The notebook produces a coverage-risk curve by sweeping confidence thresholds. This is used to show the trade-off between automatic decision coverage and prediction risk.



\---



**Robustness Stress Tests**



The robustness evaluation includes the following perturbation categories:



\- typo/noise attacks

\- character repetition

\- spacing attacks

\- leetspeak / obfuscation

\- benign quoting / contextual toxic language



A normalization and deobfuscation mitigation step is also implemented and evaluated before and after applying the defense.



\---



**Metrics**



The implementation reports:



\- F1 score for the TOXIC class

\- AUROC

\- AUPRC

\- FPR

\- FNR

\- JSON validity rate

\- DEFER rate

\- coverage

\- risk on non-deferred examples

\- latency

\- tokens/sec

\- robustness results before and after mitigation

\- prompt sensitivity

\- seed sensitivity for Self-Consistency



\---



**Repository Structure**



├── README.md

├── notebooks/

│   └── Final\_01\_setup\_and\_dataset.ipynb

├── data/

│   ├── raw/

│   ├── processed/

│   └── splits/

├── prompts/

│   └── direct\_prompt.txt

├── src/

│   ├── json\_validator.py

│   ├── robustness\_attacks.py

│   ├── mitigation.py

│   └── cli\_demo.py

├── results/

│   ├── predictions/

│   └── metrics/

├── plots/

└── report/



Some folders and files are generated automatically after running the notebook.



\---



**How to Run**



**1. Open the notebook in Google Colab**



Upload the notebook to Google Drive and open it with Google Colab.



**2. Select GPU runtime**



In Google Colab:



Runtime → Change runtime type → T4 GPU



Then restart the runtime.



**3. Add Hugging Face token**



The model requires a Hugging Face access token.



In Colab:



Secrets → Add new secret





Add the following secret:



Name: HF\_TOKEN

Value: your\_huggingface\_token





The token must have read access.



The Hugging Face account must also have access to google/gemma-2-2b-it





**4. Run the notebook**



Runtime → Run all



The notebook will:



1\. mount Google Drive

2\. create the project folders

3\. install/load required packages

4\. load the Gemma model with 4-bit quantization

5\. load and prepare the dataset

6\. run Direct Generation

7\. run Log-likelihood Scoring

8\. run Self-Consistency

9\. evaluate DEFER and coverage-risk

10\. run robustness stress tests

11\. apply mitigation

12\. generate metrics, plots, source files, and demo CLI files



\---



**Main Output Files**



results/metrics/abc\_methods\_comparison\_validation\_100.csv

results/metrics/coverage\_risk\_curve\_validation\_100.csv

results/metrics/self\_consistency\_vote\_agreement\_points.csv

results/metrics/robustness\_report\_table.csv

results/metrics/cost\_latency\_tokens\_table.csv

results/metrics/consistency\_analysis.csv

results/metrics/direct\_prompt\_sensitivity\_details.csv

results/metrics/self\_consistency\_seed\_sensitivity\_details.csv



Prediction files are saved under results/predictions/



Plots are saved under plots/



Important generated plots include:



plots/coverage\_risk\_curve\_validation\_100\_final.png

plots/robustness\_f1\_before\_after\_clean.png





**Demo CLI**



A simple demo CLI is provided under src/cli\_demo.py



Example usage:



python src/cli\_demo.py --text "You are an idiot."





The CLI returns a moderation decision containing:



\- label

\- category

\- confidence

\- short rationale

\- JSON validity status

\- latency

\- tokens/sec



\---



**Reproducibility Notes**



The notebook uses fixed random seeds where applicable.



Some minor variation may still appear in Self-Consistency results because that mechanism uses sampled generation with temperature.



The recommended reproduction environment is Google Colab + T4 GPU



Running locally is possible only if the machine has a compatible CUDA GPU and the required Python/CUDA dependencies installed.



\---



**Report**



The final report should be placed under report/





**Academic integrity statement:** The implementation, experiments, evaluation design, and interpretation of results were completed by the project team. AI tools were used only for assistance in debugging, wording, and structuring, while all critical implementation choices, experiment execution, and final verification were performed by the authors.

