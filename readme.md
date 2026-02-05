# fileutils

[![PyPi Version](https://img.shields.io/pypi/v/fileutils-dir.svg)](https://pypi.org/project/fileutils-dir/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/fileutils-dir.svg)](https://pypi.org/project/fileutils-dir/)

A minimalist, fluent Python library for listing and filtering files.

The **fileutils** library provides a clean, chainable interface to explore directories, filter by extensions, or utilize predefined file categories.

---

## Features

- **Fluent API**: Chainable methods designed for high readability and maintainability.
- **Smart Filtering**: Filter by extension or semantic categories (e.g., `code`, `data`, `image`).
- **Recursive Support**: Deep-search directory structures with a single method call.
- **Directory Trees**: Generate nested dictionary representations of folder structures.
- **Directory Filtering**: Targeted listing of subdirectories with the same fluent syntax.
- **Hidden Files**: Comprehensive control over the visibility of dotfiles.
- **Modern Python**: Built-in support for `pathlib.Path` and comprehensive type hinting.

---

## Installation

```bash
pip install fileutils-dir
```

---

## Usage

The `in_dir` function returns a query object, providing a descriptive and readable approach to listing or counting files.

### 1. Basic Listing
```python
from fileutils import in_dir

# List all files in the current directory
files = in_dir().list()

# List all Python files
python_files = in_dir(ext="py").list()
```

### 2. Semantic Filtering
Filter files based on their purpose rather than just file extensions.
```python
# List all images and videos
media = in_dir(dtype=["image", "video"]).list()

# Count all data files in a specific folder
count = in_dir(path="data", dtype="data").count()
```

### 3. Recursive and Hidden Files
```python
# Find all configuration files recursively, including hidden files
config_files = (
    in_dir(path="project")
    .recursive()
    .show_hidden()
    .list()
)
```

### 4. Directory Structures (Tree)
Generate a nested dictionary representing the directory structure.
```python
# Get a tree representation of your project
structure = in_dir("src/").recursive().tree()
```

### 5. Listing Directories
Easily switch to listing subdirectories instead of files.
```python
# List all subdirectories
folders = in_dir().dirs().list()
```

---

## API Reference

### `in_dir(path=".", *, ext=None, dtype=None)`

Initializes a `DirQuery` object.

- **`path`**: The target directory path (defaults to current directory `"."`).
- **`ext`**: A string or list of extensions (e.g., `"py"`, `[".js", "ts"]`).
- **`dtype`**: A string or list of file categories (e.g., `"code"`, `"image"`).

### `DirQuery` Methods

- **`.recursive()`**: Configures the query to traverse all subdirectories.
- **`.dirs()`**: Configures the query to match directories instead of files.
- **`.show_hidden()`**: Includes files starting with a dot (`.`) in the results.
- **`.tree()`**: Executes the query and returns a nested dictionary representation of the directory.
- **`.list()`**: Executes the query and returns a `list[str]` of matching paths.
- **`.count()`**: Executes the query and returns the total number of matching items.

---

## Supported Categories (`dtype`)

| Category | Extensions |
| :--- | :--- |
| `image` | .jpg, .jpeg, .png, .webp, .bmp, .gif, .tiff |
| `text` | .txt, .md, .rst, .log |
| `pdf` | .pdf |
| `doc` | .doc, .docx, .odt |
| `sheet` | .xls, .xlsx, .ods, .csv |
| `presentation` | .ppt, .pptx, .odp |
| `code` | .py, .js, .ts, .java, .c, .cpp, .h, .go, .rs, .rb, .php, .sh |
| `data` | .json, .yaml, .yml, .xml, .toml |
| `audio` | .mp3, .wav, .flac, .ogg, .aac, .m4a |
| `video` | .mp4, .mkv, .avi, .mov, .webm |
| `archive` | .zip, .tar, .gz, .bz2, .7z, .rar |

---

## License

This project is licensed under the MIT License.
