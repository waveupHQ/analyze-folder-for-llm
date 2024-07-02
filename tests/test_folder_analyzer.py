import os
import tempfile
import pytest
from analyze_folder_for_llm.main import FolderAnalyzer, PresetConfig


@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def create_file(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def test_analyze_folder(temp_directory):
    preset = PresetConfig(exclude=["exclude_dir"], include=["*.py", "README.md"])
    analyzer = FolderAnalyzer(temp_directory, preset)

    create_file(os.path.join(temp_directory, "README.md"), "# Test Project")
    create_file(os.path.join(temp_directory, "main.py"), "print('Hello, World!')")
    create_file(
        os.path.join(temp_directory, "exclude_dir", "excluded.py"),
        "# This should be excluded",
    )
    create_file(os.path.join(temp_directory, "test.txt"), "This should be excluded")

    analysis = analyzer.analyze_folder()

    assert any(
        item["path"] == "README.md" for item in analysis["structure"]
    ), "README.md should be in the structure"
    assert any(
        item["path"] == "main.py" for item in analysis["structure"]
    ), "main.py should be in the structure"
    assert not any(
        "exclude_dir" in item["path"] for item in analysis["structure"]
    ), "exclude_dir should not be in the structure"
    assert not any(
        item["path"] == "test.txt" for item in analysis["structure"]
    ), "test.txt should not be in the structure"
    assert analysis["readme"] == "# Test Project", "README content should be correct"
    assert (
        analysis["file_contents"]["main.py"] == "print('Hello, World!')"
    ), "main.py content should be correct"


def test_folder_analyzer_initialization(temp_directory):
    preset = PresetConfig(exclude=["exclude_dir"], include=["*.py"])
    analyzer = FolderAnalyzer(temp_directory, preset)
    assert analyzer.path == os.path.abspath(temp_directory)
    assert analyzer.exclude == {"exclude_dir"}
    assert analyzer.include == {"*.py"}


def test_should_process_file(temp_directory):
    preset = PresetConfig(exclude=["exclude_dir"], include=["*.py"])
    analyzer = FolderAnalyzer(temp_directory, preset)

    # Test files that should be processed
    assert analyzer.should_process_file(
        os.path.join(temp_directory, "test.py")
    ), "Should process test.py"
    assert analyzer.should_process_file(
        os.path.join(temp_directory, "subfolder", "test.py")
    ), "Should process subfolder/test.py"

    # Test files that should not be processed
    assert not analyzer.should_process_file(
        os.path.join(temp_directory, "test.txt")
    ), "Should not process test.txt"
    assert not analyzer.should_process_file(
        os.path.join(temp_directory, "exclude_dir", "test.py")
    ), "Should not process files in exclude_dir"

    # Additional tests to ensure correct behavior
    assert not analyzer.should_process_file(
        os.path.join(temp_directory, "exclude_dir", "subdir", "test.py")
    ), "Should not process files in subdirectories of exclude_dir"
    assert analyzer.should_process_file(
        os.path.join(temp_directory, "include_dir", "test.py")
    ), "Should process .py files in non-excluded directories"
    assert not analyzer.should_process_file(
        os.path.join(temp_directory, "include_dir", "test.txt")
    ), "Should not process non-.py files in non-excluded directories"


def test_generate_structured_output(temp_directory):
    preset = PresetConfig()
    analyzer = FolderAnalyzer(temp_directory, preset)

    create_file(os.path.join(temp_directory, "README.md"), "# Test Project")
    create_file(os.path.join(temp_directory, "main.py"), "print('Hello, World!')")

    analysis = analyzer.analyze_folder()
    output = analyzer.generate_structured_output(analysis)

    assert "folder_info" in output, "Output should contain folder_info"
    assert "readme_summary" in output, "Output should contain readme_summary"
    assert "file_structure" in output, "Output should contain file_structure"
    assert "analysis_prompts" in output, "Output should contain analysis_prompts"
    assert "Test Project" in output, "Output should contain README content"
    assert "main.py" in output, "Output should mention main.py"


# Add more tests as needed
