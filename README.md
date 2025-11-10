# Dream-Park-Backend

## 📦 Installation

1. **Create and activate a virtual environment** (recommended):
```bash
python -m venv .venv
```
2. Activate the new virtual environment so that any Python command you run or package you install uses it.

```bash
.venv\Scripts\Activate.ps1
```
3. Install the following packages:
```bash
pip install "fastapi[standard]"
pip install uvicorn
pip install pydantic
```
4. Then we activate the environment again using step 2.

## Running the fastAPI

```bash
uvicorn main:app --reload
```

## Running unit test
```bash
python -m unittest discover -s tests
```