#!/bin/bash

# USE THIS SCRIPT TO MODIFY CODE ONLY (INSIDE ZIP PACKAGE), AFTER RUNNING ./make_lambda_package.sh AT LEAST ONCE

source config.sh

unzip ${ZIP_PACKAGE_PATH} -d ${PACKAGE_PATH}/package

cd ${PACKAGE_PATH}/package
## WARNING: NOT GENERIC BELOW
rm -r mobiledet_lambda.py src ${IMAGE_FILE}
####
cd -

cp -r ${LAMBDA_CODE}/* ${INPUT_IMAGE_PATH} ${PACKAGE_PATH}/package

cd ${PACKAGE_PATH}/package
zip -r ../package.zip .
cd ..

mv package.zip ${ZIP_PACKAGE}

rm -r package



