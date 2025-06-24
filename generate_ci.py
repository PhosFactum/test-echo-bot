# generate_ci.py

import subprocess
from pathlib import Path

# Новый путь для сгенерированного workflow
GEN_WORKFLOW_FILE = Path(".github") / "workflows" / "ci_gen.yml"

# Встроенный шаблон CI/CD для ci_gen.yml
CI_TEMPLATE = """\
name: CI Pipeline Generated

on:
  push:
    branches:
      - main

jobs:
  test-and-build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Cache pip packages
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: pytest --maxfail=1 --disable-warnings -q

      - name: Build Docker image
        run: docker build --tag telegram-echo-bot:latest .

      - name: Show Docker images
        run: docker images
"""

def generate_ci():
    # Убедимся, что папка для workflow существует
    GEN_WORKFLOW_FILE.parent.mkdir(parents=True, exist_ok=True)
    # Запишем шаблон в ci_gen.yml
    GEN_WORKFLOW_FILE.write_text(CI_TEMPLATE, encoding="utf-8")
    print(f"✔ Generated workflow: {GEN_WORKFLOW_FILE}")

def commit_and_push():
    subprocess.run(["git", "add", str(GEN_WORKFLOW_FILE)], check=True)
    subprocess.run(["git", "commit", "-m", "chore: add generated CI workflow"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("✔ Committed & pushed ci_gen.yml")

if __name__ == "__main__":
    generate_ci()
    commit_and_push()

