# onnx-decomposer_local

## Local Execution

To be safe, you can use a Python Virtual Environment (venv).

Install requirements:
```bash
pip install -r requirements.txt
```

From `root`, run the following:
```bash
export PYTHONPATH=$PYTHONPATH:"$PWD":"$PWD/src"
cd src
python3 main.py
```


## Execution on AWS Lambda

```bash
cd src/aws
```

```bash
./create_python_venv.sh
source venv/bin/activate
```

Before creating the Lambda package, make sure `config.sh` and `project_name.py` have been configured correctly.
To create the whole deployment Lambda package from scratch:
```bash
./make_lambda_package.sh
```

Once the package has been created, you can modify code only with:
```bash
./modify_code_only.sh
```

To create the Lambda function on AWS:
```bash
./create_lambda_function.sh
```

Before invoking the Lambda function, make sure you have run the code locally, so that `event0.json` is the correct one.
To invoke the Lambda function (run as many times as there are layers):
```bash
./invoke_lambda_function.sh -l <layer_number>
```

