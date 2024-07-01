from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="analyze-folder-for-llm",
    version="0.1.0",
    author="jeblister",
    author_email="jeblister@waveup.dev",
    description="A tool for analyzing folder structures and content for use with large context on LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/waveuphq/analyze-folder-for-llm",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pydantic>=2.7.4,<3.0.0",
        "typer>=0.12.3,<0.13.0",
        "rich>=13.7.1,<14.0.0",
        "pyyaml>=6.0.1,<7.0.0",
    ],
    extras_require={
        "dev": ["pytest", "black"],
    },
    include_package_data=True,
    package_data={
        "analyze_folder_for_llm": ["preset.yaml"],
    },
    entry_points={
        "console_scripts": [
            "folder_to_llm=analyze_folder_for_llm.main:app",
        ],
    },
)
