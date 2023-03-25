# onnx-decomposer_local

First see: [README_preliminaries.md](README_preliminaries.md)

## Init Configuration

First, you need to configure the following file as needed:
- `general_config.ini`
- `projects/<projectname>/<projectname>_config.ini`
- `projects/<projectname>/<projectname>_steps.py`

## Execution

To be safe, it is recommended to use a Python Virtual Environment (venv): `python3 -m venv venv`

You can activate the virtual environment with `source venv/bin/activate`       
You can deactivate the virtual environment with `deactivate`

Install requirements:
```bash
pip install -r requirements.txt
```

From the `root` of the project (`onnx-decomposer_local` folder), run the following commands:
```bash
export PYTHONPATH=$PYTHONPATH:"$PWD":"$PWD/src"
cd src
```

Start the execution:
```bash
python3 main.py
```

## AWS-related steps

To go through these steps, you will need a functional AWS account. 
For simple workloads and models, a free tier account is sufficient.         

At the end of the execution, ONNX slices are uploaded to AWS S3 (AWS Cloud Storage).        
For this step to complete, you will have to create an S3 bucket.
Configure the following file with the AWS region you have selected and the name of the S3 bucket:
`<projectname>_config.ini`