#!/bin/bash

#DO NOT FORGET TO RUN THIS SCRIPT INSIDE A PYTHON VENV !!!

source config.sh

########### INITIALIZATION ###########
#if [[ -d "./${SLICE_PATH}" ]]; then
#  rm -r ${SLICE_PATH}
#fi
if [[ -d "${PACKAGE_PATH}" ]]; then
  rm -r ${PACKAGE_PATH}
fi

if [[ ! -d "./packages" ]]; then
  mkdir packages
fi

if [[ ! -d "${PACKAGE_PATH}" ]]; then
  mkdir ${PACKAGE_PATH}
fi

#mkdir ${SLICE_PATH}


########### MAIN ###########
#cp -a ${LAMBDA_CODE} ${SLICE_PATH}

pip install -Iv --target ${PACKAGE_PATH}/package numpy onnxruntime onnx protobuf==3.20.2
#pip install -Iv --target ${PACKAGE_PATH}/package numpy

#cp -r ${LAMBDA_CODE}/* ${MODEL} ${INPUT_IMAGE_PATH} ${PACKAGE_PATH}/package
cp -r ${LAMBDA_CODE}/* ${INPUT_IMAGE_PATH} ${PACKAGE_PATH}/package

cd ${PACKAGE_PATH}/package
zip -r ../package.zip .
cd ..

mv package.zip ${ZIP_PACKAGE}

rm -r package


