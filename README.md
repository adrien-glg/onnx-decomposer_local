# onnx-decomposer

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

```bash
./make_lambda_package.sh
```

```bash
./create_lambda_function.sh
```

```bash
./invoke_lambda_function.sh
./invoke_lambda_function_2.sh
```

