# Analyze Folder for LLM

Analyze Folder for LLM is a Python library designed to collect text and code from a folder for use as context with large context Language Models (LLMs). This tool efficiently fetches README files, folder structures, and non-binary file contents, providing structured outputs complete with pre-formatted prompts to guide further analysis of the folder's content.

## Installation

You can install Analyze Folder for LLM using pip:

```bash
pip install analyze-folder-for-llm
```

## Usage

After installation, you can use the `folder_to_llm` command-line tool:

```bash
folder_to_llm --path "~/your_project_folder"
```

This will analyze the specified folder and generate output files in an `output` directory within the analyzed folder.

For more options:

```bash
folder_to_llm --help
```

You can also use it in your Python scripts:

```python
from analyze_folder_for_llm import folder_to_llm

result = folder_to_llm("~/your_project_folder")
print(result)
```

## Features

- Analyze folder structures
- Extract README contents
- Collect non-binary file contents
- Generate structured output for LLM consumption
- Customizable preset configurations
- Rich console output for easy readability

## Output

The tool generates two main output files in the `output` directory of the analyzed folder:

1. `folder_contents_for_llm.txt`: Contains the contents of all non-binary files in the analyzed folder.
2. `folder_analysis_for_llm.json`: Contains a structured analysis of the folder, including file structure, README summary, and analysis prompts.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
