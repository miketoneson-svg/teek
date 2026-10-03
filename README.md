# teek
Optimized Discord Token Generator with concurrent validation and proxy caching

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/miketoneson-svg/teek.git
   cd teek
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

## Run

Start the token generator:

```bash
python3 generator.py
```

You will be prompted to enter how many tokens to generate and validate. Any valid tokens found are saved to `workingtokens.txt` in the project directory.

## Requirements

- Python 3
- `requests`
- `lxml`
