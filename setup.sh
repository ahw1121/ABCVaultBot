#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "============================================"
echo "  ABC Vault Bot - First-time setup (Mac)"
echo "============================================"
echo

if command -v python3 &>/dev/null; then
  PYTHON=python3
elif command -v python &>/dev/null; then
  PYTHON=python
else
  echo "Python was not found on this Mac."
  echo
  echo "Install Python 3.10 or newer:"
  echo "  https://www.python.org/downloads/macos/"
  echo "or:  brew install python3"
  echo
  exit 1
fi

echo "Using: $($PYTHON --version)"
echo
echo "Creating virtual environment..."
if [[ ! -d .venv ]]; then
  "$PYTHON" -m venv .venv
fi

# shellcheck source=/dev/null
source .venv/bin/activate

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

if [[ ! -f config.yaml ]]; then
  cp config.example.yaml config.yaml
  echo
  echo "Created config.yaml from the example file."
  echo "Open config.yaml in TextEdit and add your ABC login, Vault key, and keywords."
  echo "See SETUP-MAC.md for step-by-step instructions."
else
  echo "config.yaml already exists - left unchanged."
fi

echo
echo "Setup complete. Edit config.yaml, then run ./run.sh on Vault day."
echo
