# `docker images | grep -E "node-api|python-api|go-api"`

## Command Breakdown

```bash
docker images | grep -E "node-api|python-api|go-api"
```

Notice that `|` appears **twice** with two different meanings depending on whether it is inside quotes or outside quotes:

1. **`docker images`** — Lists all Docker images stored locally on your machine.
2. **`|` (pipe, outside quotes)** — The shell pipe operator. It takes the output of `docker images` and sends it as input to the next command (`grep`).
3. **`grep`** — A command-line tool that searches text line-by-line and prints only the lines that match a pattern.
4. **`-E`** — Tells `grep` to use **Extended Regular Expressions** (ERE).
5. **`|` (inside `"node-api|python-api|go-api"`)** — Inside the regex pattern, `|` means **OR**. So `grep` matches any line containing `node-api`, `python-api`, **or** `go-api`.

---

## Deep Dive: Why `-E` is Used (With vs. Without `-E`)

`grep` supports two styles of pattern matching:

1. **Without `-E` (Basic mode, the default):** Characters like `|`, `+`, `?`, `(`, `)` are treated as **plain literal text**, not special search operators.
2. **With `-E` (Extended mode):** Those characters become **special regex operators** (for example, `|` means **OR**).

Suppose `docker images` outputs:

```text
node-api     latest
python-api   latest
go-api       latest
redis        latest
```

* **If you USE `-E`:**
  ```bash
  docker images | grep -E "node-api|python-api|go-api"
  ```
  `grep` understands `|` as **OR**, so it prints:
  ```text
  node-api     latest
  python-api   latest
  go-api       latest
  ```

* **If you DO NOT use `-E`:**
  ```bash
  docker images | grep "node-api|python-api|go-api"
  ```
  `grep` searches for the **exact literal string** `node-api|python-api|go-api` (including the `|` characters). Since no image is literally named that, it prints **nothing**.

* **Alternative without `-E`:** You would have to escape each `|` with a backslash (`\|`):
  ```bash
  docker images | grep "node-api\|python-api\|go-api"
  ```
  Using `-E` avoids those backslashes and keeps the command readable.
