"""The offline JSONPlaceholder example stays on the documented post fields and does not call a model."""

import ast
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLIENT = ROOT / "examples" / "api_first" / "client.py"
FIXTURE = ROOT / "examples" / "api_first" / "fixtures" / "post_1.json"


def load_client():
    spec = importlib.util.spec_from_file_location("api_first_client", CLIENT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fixture_matches_the_documented_post_fields():
    client = load_client()
    post = client.load_post()
    assert post == {
        "userId": 1,
        "id": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "body": (
            "quia et suscipit\n"
            "suscipit recusandae consequuntur expedita et cum\n"
            "reprehenderit molestiae ut ut quas totam\n"
            "nostrum rerum est autem sunt rem eveniet architecto"
        ),
    }
    assert client.FIXTURE == FIXTURE


def test_client_imports_neither_a_model_sdk_nor_an_http_library():
    tree = ast.parse(CLIENT.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert imported == {"__future__", "json", "pathlib"}


def test_client_prints_the_post_id_and_title():
    result = subprocess.run([sys.executable, str(CLIENT)], check=False, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout == "1\tsunt aut facere repellat provident occaecati excepturi optio reprehenderit\n"
    assert result.stderr == ""
