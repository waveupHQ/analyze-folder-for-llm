# Contributing to Analyze Folder for LLM

We welcome contributions to the Analyze Folder for LLM project! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```
   git clone https://github.com/waveuphq/analyze-folder-for-llm.git
   ```
3. Create a virtual environment and install the development dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   pip install -e .
   ```

## Making Changes

1. Create a new branch for your changes:
   ```
   git checkout -b your-feature-branch
   ```
2. Make your changes in the `src/analyze_folder_for_llm` directory.
3. Add or update tests in the `tests` directory to cover your changes.
4. Run the tests to ensure everything is working:
   ```
   pytest
   ```
5. Update the documentation if necessary.

## Submitting Changes

1. Commit your changes:
   ```
   git commit -am "Add your commit message here"
   ```
2. Push to your fork:
   ```
   git push origin your-feature-branch
   ```
3. Submit a pull request through the GitHub website.

## Coding Conventions

- Follow PEP 8 style guide for Python code.
- Use type hints where possible.
- Write descriptive commit messages.
- Add comments to explain complex logic or decisions.

## Reporting Bugs

- Use the GitHub issue tracker to report bugs.
- Describe the bug and include steps to reproduce if possible.
- Include information about your environment (OS, Python version, etc.).

Thank you for contributing to Analyze Folder for LLM!
