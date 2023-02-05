# onnx-decomposer_local

## Init Configuration

First, you need to configure the following file as needed:
- `projectname_config.ini`
- `projects/<projectname>/<projectname>_config.ini`
- `projects/<projectname>/<projectname>_steps.py`

## Execution

To be safe, it is recommended to use a Python Virtual Environment (venv):
```bash
python3 -m venv venv
```

You can activate the virtual environment with `source venv/bin/activate`.       
You can deactivate the virtual environment with `deactivate`.

Install requirements:
```bash
pip install -r requirements.txt
```

From `root`, run the following commands:
```bash
export PYTHONPATH=$PYTHONPATH:"$PWD":"$PWD/src"
cd src
```

Start the execution:
```bash
python3 main.py
```
