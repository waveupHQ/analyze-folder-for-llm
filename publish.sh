#!/bin/bash

# Ensure we're in the project root directory
cd "$(dirname "$0")"

# Update version number
echo "Current version:"
grep "version" setup.py
read -p "Enter new version number: " VERSION
sed -i "" "s/version=\".*\"/version=\"$VERSION\"/" setup.py
sed -i "" "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" src/analyze_folder_for_llm/__init__.py

# Clean up previous builds
rm -rf build dist *.egg-info

# Build the package
python setup.py sdist bdist_wheel

# Upload to Test PyPI
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

echo "Package uploaded to Test PyPI. Verify it works by installing:"
echo "pip install --index-url https://test.pypi.org/simple/ analyze-folder-for-llm==$VERSION"

read -p "Do you want to upload to PyPI? (y/n) " UPLOAD_TO_PYPI

if [ "$UPLOAD_TO_PYPI" = "y" ]; then
    # Upload to PyPI
    twine upload dist/*
    echo "Package uploaded to PyPI. You can now install it with:"
    echo "pip install analyze-folder-for-llm==$VERSION"
else
    echo "Skipped uploading to PyPI."
fi