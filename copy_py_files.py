import os


def concatenate_files(source_dir, output_file, exclude_script):
    with open(output_file, "w", encoding="utf-8") as outfile:
        for root, dirs, files in os.walk(source_dir):
            # Exclude __pycache__, output, and venv directories
            dirs[:] = [d for d in dirs if d not in ["__pycache__", "output", "venv"]]

            for file in files:
                if (
                    file.endswith(".py") or file == "README.md"
                ) and file != exclude_script:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, source_dir)

                    outfile.write(f"\n\n# File: {relative_path}\n")
                    outfile.write("=" * 50 + "\n\n")

                    with open(file_path, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())

                    print(f"Concatenated: {relative_path}")


if __name__ == "__main__":
    source_directory = "."  # Current directory
    prompt = """
                "What is the main purpose of this repository",
                "Are there any clear coding patterns or standards visible in the file structure?",
                "Are there any interesting or unusual files or directories in the repository structure?",
                "Based on the file contents, what are the main features or functionalities of this project?",
                "Are there any potential areas for improvement or optimization in the code?",
                "How well is the project documented? Are there comments in the code and comprehensive README instructions?",
                "Are there any security concerns visible in the repository structure or file contents?",
                "What dependencies or external libraries does this project rely on?",
                "How modular and maintainable does the codebase appear to be?"""
    output_file = "concatenated_files.txt"  # Output file

    script_name = os.path.basename(__file__)  # Name of this script

    concatenate_files(source_directory, output_file, script_name)
    print(f"Concatenation completed. Output file: {output_file}")
