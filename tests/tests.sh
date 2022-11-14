#!/bin/bash
echo "Attemping to setup projects ========================"
zifopybuilder setup-project -n testproject
zifopybuilder setup-project -n testprojectnogit --skipgit
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

for PKG in "pytest" "black" "isort" "mypy" "flake8" "pre-commit"
do
    if ! grep -q "testproject/pyproject.toml"; then
        echo "FAILED: testproject missing one or more quality tools"
        exit 999
    else
        echo "TEST PASSED"
    fi
done

#testprojectnogit
if [ -d "testproject" ]; then
    echo "FAILED: testprojectnogit should not contain a .git folder"
    exit 999
else
    echo "TEST PASSED"
fi

#testprojectremote
REMOTE=$(cd testprojectremote && git config --get remote.origin.url)
if $REMOTE != "https:://github.com/ZIFODS/test.git "; then
    echo "FAILED: testprojectremote remote URL does not equal 'https:://github.com/ZIFODS/test.git'"
    exit 999
fi

#testanalytical
if [ ! -d "testproject/data" ]; then
    echo "FAILED: testanalytical creation failed"
    exit 999
else
    echo "TEST PASSED"
fi

if [ ! -d "testproject/reports" ]; then
    echo "FAILED: testanalytical creation failed"
    exit 999
else
    echo "TEST PASSED"
fi

if [ ! -d "testproject/models" ]; then
    echo "FAILED: testanalytical creation failed"
    exit 999
else
    echo "TEST PASSED"
fi

echo "TESTS COMPLETE"
