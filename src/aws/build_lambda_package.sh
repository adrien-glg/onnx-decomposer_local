#!/bin/bash

PROJECT_NAME="mobiledet"
LAMBDA_FUNCTION="lambda_functions/mobiledet_first_slice_lambda.py"
SLICE="slice0"
INPUT_IMAGE_PATH="../../models/mobiledet/img_resized.npy"
MODEL="../../models/mobiledet/slices/mobiledet_slice0.onnx"
SLICE_PATH="packages/${PROJECT_NAME}/${SLICE}"

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

cp ${LAMBDA_FUNCTION} ${SLICE_PATH}/lambda_function.py

#pip install -Iv --target ./package numpy onnxruntime onnx protobuf==3.20.1
pip install -Iv --target ./package numpy

zip -r ${SLICE_PATH}/package.zip package

zip -g ${SLICE_PATH}/package.zip ${SLICE_PATH}/lambda_function.py ${MODEL} ${INPUT_IMAGE_PATH}

#mv package.zip mobiledet_part1.zip

rm -r package ${SLICE_PATH}/lambda_function.py


