from pathlib import Path
from typing import Iterable


FILE_TYPES = {
    "image": [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff"],
    "text": [".txt", ".md", ".rst", ".log"],
    "pdf": [".pdf"],
    "doc": [".doc", ".docx", ".odt"],
    "sheet": [".xls", ".xlsx", ".ods", ".csv"],
    "presentation": [".ppt", ".pptx", ".odp"],
    "code": [
        ".py", ".js", ".ts", ".java", ".c", ".cpp", ".h",
        ".go", ".rs", ".rb", ".php", ".sh"
    ],
    "data": [".json", ".yaml", ".yml", ".xml", ".toml"],
    "audio": [".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a"],
    "video": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "archive": [".zip", ".tar", ".gz", ".bz2", ".7z", ".rar"],
}


def in_dir(
    directories: Iterable[str] | None = None,
    extensions: Iterable[str] | None = None,
    types: Iterable[str] | None = None,
) -> list[str]:
    """
    Return files from the given directories:\n.
    - If 'directories' are not given, only the PWD is considered.
    - If `extensions` or `types` are provided, only matching files are returned.
    - If neither is provided, all files in the PWD are returned.
    """

    if directories is None:
        directories = ["."]
    if extensions is None:
        extensions = []
    if types is None:
        types = []

    normalized_extensions = {
        ext.lower() if ext.startswith(".") else f".{ext.lower()}"
        for ext in extensions
    }

    for file_type in types:
        key = file_type.strip().lower()
        try:
            normalized_extensions.update(FILE_TYPES[key])
        except KeyError:
            raise ValueError(f"Unknown file type: {file_type}")

    files_to_return: list[str] = []

    for path in directories:
        for item in Path(path).iterdir():
            if not item.is_file():
                continue

            # If no filters, accept everything
            if not normalized_extensions:
                files_to_return.append(str(item))
                continue

            # Otherwise, filter by extension
            if item.suffix.lower() in normalized_extensions:
                files_to_return.append(str(item))

    return files_to_return
