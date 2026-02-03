from collections.abc import Iterable
from pathlib import Path

FILE_TYPES = {
    "image": [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff"],
    "text": [".txt", ".md", ".rst", ".log"],
    "pdf": [".pdf"],
    "doc": [".doc", ".docx", ".odt"],
    "sheet": [".xls", ".xlsx", ".ods", ".csv"],
    "presentation": [".ppt", ".pptx", ".odp"],
    "code": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".h", ".go", ".rs", ".rb", ".php", ".sh"],
    "data": [".json", ".yaml", ".yml", ".xml", ".toml"],
    "audio": [".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a"],
    "video": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "archive": [".zip", ".tar", ".gz", ".bz2", ".7z", ".rar"],
}

def in_dir(
    path=".",
    *args,
    ext=None,
    dtype=None,
) -> list[str]:
    """
    "in_dir() accepts only one positional argument (path).
            Use keyword arguments for filters or leave empty:
            in_dir(path, ext='filetype')
            in_dir(path, dtype='data_type')
    dtype options: image, text, pdf, doc, sheet, presentation, code, data, audio, video, archive
    """
    if args:
        raise TypeError(
            "in_dir() accepts only one positional argument (path).\n"
            "Use keyword arguments for filters or leave empty:\n"
            "  in_dir(path, ext='filetype')\n"
            "  in_dir(path, dtype='data_type')"
        )
    ext = ext or []
    dtype = dtype or []
    
    if isinstance(ext, str):
        ext = [ext]
    if isinstance(dtype, str):
        dtype = [dtype]

    normalized_extensions = {
        e.lower() if e.startswith(".") else f".{e.lower()}"
        for e in ext
    }

    for file_type in dtype:
        key = file_type.strip().lower()
        if key not in FILE_TYPES:
            raise ValueError(
                f"Unknown file type: {file_type}. "
                f"Valid types: {', '.join(FILE_TYPES)}"
            )
        normalized_extensions.update(FILE_TYPES[key])

    files: list[str] = []

    for item in Path(path).iterdir():
        if item.is_file() and (
            not normalized_extensions or item.suffix.lower() in normalized_extensions
        ):
            files.append(str(item))

    return files

