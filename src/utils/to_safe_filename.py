import re

import unicodedata

# Windows / macOS / Linux common forbidden characters
_INVALID_CHARS = re.compile(r'[\\/:*?"<>|]+')
_WHITESPACE = re.compile(r"\s+")

# Windows reserved filenames (case-insensitive)
_WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def to_safe_filename(name: str, replacement: str = "_") -> str:
    """
    Convert a string into a filesystem-safe filename stem.

    This function assumes the input string does NOT include a file extension.
    The result is safe to use on Windows, macOS, and Linux.

    Args:
        name: Original filename stem.
        replacement: Replacement string for invalid characters.

    Returns:
        A sanitized, filesystem-safe filename stem.
    """
    if not name:
        return "unnamed"
    
    # Normalize unicode (e.g. full-width, accents)
    name = unicodedata.normalize("NFKD", name)
    
    # Remove non-printable characters
    name = "".join(c for c in name if c.isprintable())
    
    # Replace forbidden characters
    name = _INVALID_CHARS.sub(replacement, name)
    
    # Collapse whitespace
    name = _WHITESPACE.sub(replacement, name)
    
    # Strip leading/trailing dots, spaces, and underscores
    name = name.strip("._ ")
    
    # Avoid Windows reserved names
    if name.upper() in _WINDOWS_RESERVED_NAMES:
        name = f"{name}_"
    
    return name or "unnamed"
