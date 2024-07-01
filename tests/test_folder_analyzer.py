import os
import tempfile
import pytest
from analyze_folder_for_llm.main import FolderAnalyzer, PresetConfig


@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def create_file(path, content=""):
    with open(path, "w") as f:
        f.write(content)


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

    # Test with different preset configurations
    preset_no_include = PresetConfig(exclude=["exclude_dir"])
    analyzer_no_include = FolderAnalyzer(temp_directory, preset_no_include)
    assert analyzer_no_include.should_process_file(
        os.path.join(temp_directory, "test.py")
    ), "Should process test.py without include patterns"
    assert analyzer_no_include.should_process_file(
        os.path.join(temp_directory, "README.md")
    ), "Should process README.md without include patterns"
    assert not analyzer_no_include.should_process_file(
        os.path.join(temp_directory, "test.txt")
    ), "Should not process test.txt without include patterns"


# ... (rest of the tests remain the same)
