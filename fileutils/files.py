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


class DirQuery:
    """Query object for listing files in a directory."""

    def __init__(self, path=".", *, ext=None, dtype=None):
        """Create a directory query with optional filters."""
        self._dirs = False
        self._recursive = False
        self.path = Path(path)
        self._show_hidden = False

        ext = ext or []
        dtype = dtype or []

        if isinstance(ext, str):
            ext = [ext]
        if isinstance(dtype, str):
            dtype = [dtype]

        self.normalized_extensions = {
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
            self.normalized_extensions.update(FILE_TYPES[key])

    def show_hidden(self):
        """Include hidden files in results."""
        self._show_hidden = True
        return self

    def tree(self) -> dict[str, object]:
        """Return a nested dictionary representing the directory tree."""
        tree: dict[str, object] = {}

        iterator = (
            self.path.rglob("*")
            if self._recursive
            else self.path.iterdir()
        )

        for item in iterator:
            # files only (tree is file-centric)
            if not item.is_file():
                continue

            if not self._show_hidden and item.name.startswith("."):
                continue

            if self.normalized_extensions and item.suffix.lower() not in self.normalized_extensions:
                continue

            rel = item.relative_to(self.path)
            parts = rel.parts

            cursor = tree
            for part in parts[:-1]:
                cursor = cursor.setdefault(part, {})

            cursor[parts[-1]] = None

        return tree

    def list(self) -> list[str]:
        """Return matching subdirectories or files based on filters."""
        results: list[str] = []

        iterator = (
            self.path.rglob("*")
            if self._recursive
            else self.path.iterdir()
        )
        for item in iterator:
            if self._dirs:
                if not item.is_dir():
                    continue
            else:
                if not item.is_file():
                    continue
            if not self._show_hidden and item.name.startswith("."):
                continue
            if not self._dirs:
                if (
                        self.normalized_extensions
                        and item.suffix.lower() not in self.normalized_extensions
                ):
                    continue

            results.append(str(item))

        return results

    def count(self) -> int:
        """Return number of matching files."""
        return len(self.list())

    def recursive(self):
        """
        Includes all files in directory recursively.
        """
        self._recursive = True
        return self

    def dirs(self):
        """
        Includes only the subdirectories in the directory.
        """
        self._dirs = True
        return self


def in_dir(path=".", *args, ext=None, dtype=None) -> DirQuery:
    """
    Helps list/count all subdirectories/files in a directory with support for filters such as extensions and types.
    Types include: image, text, audio, video, code, presentation, data, archive, sheet, data.
    """


    if args:
        raise TypeError(
            "in_dir() accepts only one positional argument (path).\n"
            "Use keyword arguments for filters:\n"
            "  in_dir(path, ext='py')\n"
            "  in_dir(path, dtype='image')"
        )

    return DirQuery(path, ext=ext, dtype=dtype)
