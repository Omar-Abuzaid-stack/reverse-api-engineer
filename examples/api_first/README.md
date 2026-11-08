# API-first example

JSONPlaceholder publishes `GET /posts/1` with no authentication. The response fields are `userId`, `id`, `title`, and `body`. This example reads a saved copy of that response instead of capturing a browser session or asking a model to write a client.

```bash
uv run python examples/api_first/client.py
```

`fixtures/post_1.json` was copied from `https://jsonplaceholder.typicode.com/posts/1`. The client does not take a URL argument and does not send a request.

This script makes no model call. That is true of this file only: it imports `json` and `pathlib` and reads one fixture. A browser capture was not run, so there is no measured token or dollar delta against agent mode.
