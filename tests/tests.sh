#!/bin/bash
echo "Attemping to setup projects ========================"
zifopybuilder setup-project -n testproject
zifopybuilder setup-project -n testprojectremote --remote https:://github.com/ZIFODS/test.git
zifopybuilder setup-project -n testanalytical --analytical

echo "Running post-setup checks ========================"
#testproject
if [ ! -d "testproject" ]; then
    echo "FAILED: testproject creation failed"
    exit 999
else
    echo "TEST PASSED"
fi

if [ ! -f "testproject/.pre-commit-config.yaml" ]; then
    echo "FAILED: testproject missing pre-commit config"
    exit 999
else
    echo "TEST PASSED"
fi

if [ ! -f "testproject/.gitignore" ]; then
    echo "FAILED: testproject missing gitignore"
    exit 999
else
    echo "TEST PASSED"
fi

if [ ! -d "testproject/.git" ]; then
    echo "FAILED: testproject git init failed"
    exit 999
else
    echo "TEST PASSED"
fi

#testprojectremote
REMOTE=$(cd testprojectremote && git config --get remote.origin.url)
if "${REMOTE}" != "https:://github.com/ZIFODS/test.git"; then
    echo "FAILED: testprojectremote remote URL does not equal 'https:://github.com/ZIFODS/test.git'"
    exit 999
fi

#testanalytical
if [ ! -d "testanalytical/data" ]; then
    echo "FAILED: testanalytical creation failed"
    exit 999
else
    echo "TEST PASSED"
fi

if [ ! -d "testanalytical/reports" ]; then
    echo "FAILED: testanalytical creation failed"
    exit 999
else
    echo "TEST PASSED"
fi

if [ ! -d "testanalytical/models" ]; then
    echo "FAILED: testanalytical creation failed"
    exit 999
else
    echo "TEST PASSED"
fi

echo "TESTS COMPLETE"
