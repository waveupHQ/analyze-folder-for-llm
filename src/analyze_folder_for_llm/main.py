import os
from typing import List, Optional, Dict
import fnmatch
import json
from pydantic import BaseModel, Field
import yaml
from rich.console import Console
import typer
from rich.panel import Panel

app = typer.Typer()
console = Console()


class PresetConfig(BaseModel):
    # Using Pydantic for automatic validation of configuration
    exclude: List[str] = Field(default_factory=list)
    include: List[str] = Field(default_factory=list)


class FolderAnalyzer:
    def __init__(
        self,
        path: str,
        preset: PresetConfig,
        exclude: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
    ):
        self.path = os.path.abspath(os.path.expanduser(path))
        self.exclude = set(exclude or preset.exclude)
        self.include = set(include or preset.include)
        self.output_dir = os.path.join(self.path, "output")
        os.makedirs(self.output_dir, exist_ok=True)

    def should_process_file(self, file_path: str) -> bool:
        relative_path = os.path.relpath(file_path, self.path)
        path_parts = relative_path.split(os.sep)

        print(f"Checking file: {relative_path}")
        print(f"Exclude patterns: {self.exclude}")
        print(f"Include patterns: {self.include}")

        # Check if any part of the path is in the exclude list
        if any(excluded in path_parts for excluded in self.exclude):
            print(f"File excluded: {relative_path}")
            return False

        # If include patterns are specified, check if the file matches any
        if self.include:
            should_include = any(
                self._match_pattern(relative_path, pattern) for pattern in self.include
            )
            print(f"Include check result: {should_include}")
            return should_include

        # Default include logic for Python files and README
        default_include = (
            file_path.endswith(".py")
            or os.path.basename(file_path).lower() == "readme.md"
        )
        print(f"Default include check result: {default_include}")
        return default_include

    def _match_pattern(self, path: str, pattern: str) -> bool:
        result = fnmatch.fnmatch(path, pattern)
        print(f"Matching {path} against {pattern}: {result}")
        return result

    def analyze_folder(self) -> dict:
        analysis = {"structure": [], "file_contents": {}, "readme": None}

        for root, dirs, files in os.walk(self.path):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in self.exclude]

            for file in files:
                file_path = os.path.join(root, file)
                if self.should_process_file(file_path):
                    relative_path = os.path.relpath(file_path, self.path)
                    analysis["structure"].append(
                        {"path": relative_path, "type": "file"}
                    )

                    with open(file_path, "r", encoding="utf-8") as infile:
                        content = infile.read()
                        if file.lower() == "readme.md":
                            analysis["readme"] = content
                        else:
                            analysis["file_contents"][relative_path] = content

        return analysis

    def generate_structured_output(self, analysis: dict) -> str:
        # Create a structured JSON output for easy consumption by LLMs
        output = {
            "folder_info": {"path": self.path},
            "readme_summary": (
                analysis["readme"][:500] + "..."
                if analysis["readme"]
                else "No README found"
            ),
            "file_structure": [item["path"] for item in analysis["structure"]],
            "analysis_prompts": [
                "What is the main purpose of this project based on the README and file structure?",
                "What programming languages are primarily used in this project?",
                "Are there any interesting or unusual files or directories in the folder structure?",
                "Based on the file contents, what are the main features or functionalities of this project?",
                "How well is the project documented? Are there comments in the code and comprehensive README instructions?",
                "What dependencies or external libraries does this project rely on?",
                "How modular and maintainable does the codebase appear to be?",
                "Are there any potential security concerns visible in the folder structure or file contents?",
                "What aspects of this project might be particularly relevant for an LLM to focus on?",
                "How could this project's structure or documentation be improved for better LLM analysis?",
            ],
        }
        return json.dumps(output, indent=2)

    def generate_content_file(self, analysis: dict) -> None:
        # Create a single file with all relevant content for easy LLM processing
        filename = os.path.join(self.output_dir, "folder_contents_for_llm.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Contents of folder: {self.path}\n\n")

            if analysis["readme"]:
                f.write("README:\n")
                f.write("=" * 50 + "\n")
                f.write(analysis["readme"])
                f.write("\n\n" + "=" * 50 + "\n\n")

            for path, content in analysis["file_contents"].items():
                f.write(f"File: {path}\n")
                f.write("-" * 50 + "\n")
                f.write(content)
                f.write("\n\n" + "-" * 50 + "\n\n")

        console.print(f"[green]Folder contents saved to {filename}[/green]")


def load_preset(preset_file: str) -> PresetConfig:
    # Load preset configuration from YAML file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    preset_path = os.path.join(script_dir, preset_file)
    if os.path.exists(preset_path):
        with open(preset_path, "r") as f:
            data = yaml.safe_load(f)
        return PresetConfig(**data)
    return PresetConfig()


@app.command()
def folder_to_llm(
    path: str = typer.Option(".", "--path", help="Path to the folder to analyze"),
    preset: str = typer.Option(
        "preset.yaml", "--preset", help="Path to the preset YAML file"
    ),
    exc: Optional[List[str]] = typer.Option(
        None, "--exc", help="Additional folders to exclude"
    ),
    inc: Optional[List[str]] = typer.Option(
        None, "--inc", help="Additional folders and files to include"
    ),
):
    """Analyze a folder and prepare its contents for LLM processing."""
    preset_config = load_preset(preset)
    analyzer = FolderAnalyzer(path, preset_config, exc, inc)
    analysis = analyzer.analyze_folder()
    structured_output = analyzer.generate_structured_output(analysis)

    console.print(Panel.fit("Structured Output", title="Analysis Result"))
    console.print(structured_output)

    output_file = os.path.join(analyzer.output_dir, "folder_analysis_for_llm.json")
    with open(output_file, "w") as f:
        f.write(structured_output)
    console.print(f"[green]Analysis saved to {output_file}[/green]")

    analyzer.generate_content_file(analysis)

    return json.loads(structured_output)


if __name__ == "__main__":
    app()
