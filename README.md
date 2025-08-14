
# QuickShort · URL Shortener (Flask + SQLite + Docker)

A minimal, clean URL shortener built with Flask. Features:

- Shorten long URLs to short codes
- Redirect via `/<code>`
- SQLite persistence
- Click counter
- Bootstrap-based UI
- Docker one-command start

---

## Run Locally (Python)

```bash
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```

## Run with Docker (One Command)

```bash
docker-compose up --build
# open http://127.0.0.1:5000
```

## Project Structure

```text
app.py
data.db (auto-created)
templates/
  base.html
  index.html
  404.html
Dockerfile
docker-compose.yml
requirements.txt
```

## Notes

- The app auto-creates `data.db` on first run.
- To persist DB outside container, map a volume in `docker-compose.yml`:
  ```yaml
  volumes:
    - ./data.db:/app/data.db
  ```

## Deploy Hints (Render/Railway/AWS)

- Set `PORT` env var if your platform requires it.
- For AWS EC2 + Docker:
  ```bash
  docker-compose up --build -d
  ```
