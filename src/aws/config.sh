#!/bin/bash

### TO BE CONFIGURED MANUALLY ###
PROJECT_NAME="mobiledet"
NUMBER_OF_SLICES=2
S3_BUCKET="onnx-mobiledet-bucket"
#################################

FUNCTION_NAME="${PROJECT_NAME}_${NUMBER_OF_SLICES}_slices"

LAMBDA_CODE="lambda_code/${PROJECT_NAME}"
#SLICE="slice0"
IMAGE_FILE="img_resized.npy"
INPUT_IMAGE_PATH="../../models/mobiledet/${IMAGE_FILE}"
#MODEL="../../models/mobiledet/slices/mobiledet_slice0.onnx"
#SLICE_PATH="packages/${PROJECT_NAME}/${SLICE}"
PACKAGE_PATH="./packages/${PROJECT_NAME}"
ZIP_PACKAGE="${FUNCTION_NAME}.zip"
ZIP_PACKAGE_PATH="${PACKAGE_PATH}/${ZIP_PACKAGE}"



