## Preliminaries

Move to the directory with the name of your project (create the directory if needed), containing the Jupyter Notebook
and the ML model:
```bash
cd projects/<projectname>
```

Convert the Jupyter Notebook to Python:
```bash
jupyter nbconvert --to python <jupyter_notebook.ipynb>
```

Convert the model to ONNX format:
```bash
python3 <projectname>_onnx_conversion.py
```

## Convert input

```bash
python3 <projectname>_input_preprocessing.py
```

## Create and fill in the following files

```bash
<projectname>_config.ini
<projectname>_requirements.txt
<projectname>_steps.py
```
