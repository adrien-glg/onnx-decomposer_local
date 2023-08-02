# onnx-decomposer_local

First see: [README_preliminaries.md](README_preliminaries.md)

## Init Configuration

If not already done, configure the following files as needed:
- `general_config.ini`
- `projects/<projectname>/<projectname>_config.ini`
- `projects/<projectname>/<projectname>_steps.py`

## Decomposition and inference

To be safe, it is recommended to use a Python Virtual Environment (venv): `python3 -m venv venv`        
You can activate the virtual environment with `source venv/bin/activate`            
You can deactivate the virtual environment with `deactivate`

From the `root` of the project (`onnx-decomposer_local` folder), run the following commands:        
Install requirements:
```bash
pip install -r requirements.txt
```

Configure the Python path:
```bash
export PYTHONPATH=$PYTHONPATH:"$PWD":"$PWD/src"
cd src
```

Start the decomposition and inference:
```bash
python3 main.py  # TODO talk about the different modes
```

## Conformity checks

To check the temporary storage size violation, we need to check the maximum slice size:
```bash
# TODO
```

## AWS-related steps

To go through these steps, you will need a functional AWS account. 
For simple workloads and models, a free tier account is sufficient.         

At the end of the execution, ONNX slices are uploaded to AWS S3 (AWS Cloud Storage).        
For this step to complete, you will have to create an S3 bucket.
Configure the file `<projectname>_config.ini` with the AWS region you have selected and the name of the S3 bucket.

## References

This project includes code and content from the following sources:
- [tensorflow-onnx](https://github.com/onnx/tensorflow-onnx/)
```bash
# TODO add other references
```
