#!/bin/bash

#DO NOT FORGET TO RUN THIS SCRIPT INSIDE A PYTHON VENV !!!

PROJECT_NAME="mobiledet"
LAMBDA_CODE="lambda_code/mobiledet"
SLICE="slice0"
INPUT_IMAGE_PATH="../../models/mobiledet/img_resized.npy"
MODEL="../../models/mobiledet/slices/mobiledet_slice0.onnx"
SLICE_PATH="packages/${PROJECT_NAME}/${SLICE}"
OUTPUT_ZIP="mobiledet_slice0.zip"

########### INITIALIZATION ###########
if [[ -d "./${SLICE_PATH}" ]]; then
  rm -r ${SLICE_PATH}
fi

if [[ ! -d "./packages" ]]; then
  mkdir packages
fi

if [[ ! -d "./packages/${PROJECT_NAME}" ]]; then
  mkdir packages/${PROJECT_NAME}
fi

mkdir ${SLICE_PATH}


########### MAIN ###########
#cp -a ${LAMBDA_CODE} ${SLICE_PATH}

pip install -Iv --target ${SLICE_PATH}/package numpy onnxruntime onnx protobuf==3.20.2
#pip install -Iv --target ${SLICE_PATH}/package numpy

cp -r ${LAMBDA_CODE}/* ${MODEL} ${INPUT_IMAGE_PATH} ${SLICE_PATH}/package

cd ${SLICE_PATH}/package
zip -r ../package.zip .
cd ..

mv package.zip ${OUTPUT_ZIP}

rm -r package


