"""Read one JSONPlaceholder post from a local fixture.

JSONPlaceholder documents ``GET /posts/1`` at https://jsonplaceholder.typicode.com/posts/1.
The body in ``fixtures/post_1.json`` is a copy of that response. This client reads the
file and does not open a socket or call a model.
"""

from __future__ import annotations

import json
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "post_1.json"
FIELDS = ("userId", "id", "title", "body")


def load_post(path: Path | None = None) -> dict[str, object]:
    """Return the documented post fields from the offline fixture."""
    source = path or FIXTURE
    data = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{source} must contain a JSON object")
    missing = [field for field in FIELDS if field not in data]
    if missing:
        raise ValueError(f"{source} is missing {', '.join(missing)}")
    return {field: data[field] for field in FIELDS}


def main() -> None:
    post = load_post()
    print(f"{post['id']}\t{post['title']}")


if __name__ == "__main__":
    main()
