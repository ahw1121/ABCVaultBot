#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [[ ! -f config.yaml ]]; then
  echo "config.yaml not found."
  echo "Run ./setup.sh first, then edit config.yaml with your settings."
  exit 1
fi

if [[ ! -f .venv/bin/activate ]]; then
  echo "Setup not finished. Run ./setup.sh first."
  exit 1
fi

# shellcheck source=/dev/null
source .venv/bin/activate

echo "Starting ABC Vault Bot..."
echo "Press Ctrl+C to stop."
echo
python -m abcvaultbot -c config.yaml
echo
echo "Bot stopped."
