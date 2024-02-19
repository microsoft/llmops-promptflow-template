# Promptflow in Azure Machine Learning Pipeline

## Overview
To provide scalability and reliability, we can run promptflow in Azure Machine Learning pipeline. Azure Machine Learning provides a scalable and reliable environment to run the promptflow jobs. It also provides observability and monitoring for the pipeline runs.

Go to [Use Flow in Azure ML Pipeline Job](https://microsoft.github.io/promptflow/cloud/azureai/use-flow-in-azure-ml-pipeline.html?highlight=pipeline#directly-use-a-flow-in-a-pipeline-job) for more details.

## Prerequisites
1. Azure ML workspace 

## Steps to run the AML pipeline
1. Create an external ADLS Gen2 storage account and a container named `data` to store the input data, transient data and the output data.
2. Upload the input data  `web_classification/data/data.jsonl`` to the `data` container.
Update your .env.template in pf-in-aml-pipeline folder with the required values and rename it to .env
3. Setup a python environment with the packages mentioned in requirements.txt:
```bash
pip install -r requirements.txt
```
4. Run the following commands to execute the pipeline:
```bash
cd pf-in-aml-pipeline
python run_pipeline.py
```
5. Go to AML workspace and check the pipeline run status.