## Preliminaries

The preliminaries involve 3 main steps:
- Converting the Jupyter notebook to Python
- Converting the ML model to ONNX format
- If needed, converting the input file to a supported format

From the `root` of the project (`onnx-decomposer_local` folder):    

Configure the file `general_config.ini` with the name of the project.

Configure the Python path:
```bash
export PYTHONPATH=$PYTHONPATH:"$PWD":"$PWD/src"
```

Move to the directory with the name of the project, containing the Jupyter Notebook and the ML model:
```bash
cd projects/<projectname>
```

Configure the file `<projectname>_config.ini` as needed.

Convert the Jupyter notebook to Python:
```bash
jupyter nbconvert --to python <jupyter_notebook.ipynb>
```

Convert the ML model to ONNX format:
```bash
python3 <projectname>_onnx_conversion.py
```
If the file above does not exist, follow the conversion steps from the Jupyter notebook.

Convert the input file (not required with `efficientdet`):
```bash
python3 <projectname>_input_preprocessing.py
```

If needed, complete or modify the following file:
```bash
<projectname>_steps.py
```
