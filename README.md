# 🧮 File System Analyzer (fs-analyze)

A command-line tool to analyze and report on the structure, usage, and contents of a file system on Linux.

Built with **Python (only built-in libraries)**.

---

## 📦 Features

- 🔍 **Directory Traversal** — Recursively scans a specified directory
- 🗃️ **File Type Categorization** — Classifies files by extension (images, audio, video, etc.)
- 📊 **Size Analysis** — Calculates total size per category
- 🧾 **Permission Report** — Displays file permissions (read/write/execute)
- 🚨 **Large File Detection** — Flags files above a given size threshold
- 📁 **Ignore List** — Skips specific files or folders
- 🖨️ **CLI Output** — Optionally output save to file
- 🧪 Includes basic `pytest`-based tests

---

## 🚀 Installation

```bash
git clone https://github.com/Gor903/FileSystemAnalyzer.git
cd FileSystemAnalyzer
pip install .
```
---

## 🔧 Usage

```bash
python -m venv venv
source venv/bin/activate && pip install --upgrade pip
pip install .
fs-analyzer -h
fs-analyzer [DIRECTORY] [OPTIONS]
```

To run tests
```bash
pytest tests/test_scanner.py
```

---

### ⚙️ Options

- `-s`, `--size SIZE_MB`
  Threshold in **megabytes** to flag large files.
  Example: `--size 50` (flags files larger than 50 MB)

- `-i`, `--ignore "a,b,c"`
  Comma-separated list of files or directories to ignore during the scan.
  Example: `--ignore ".git,node_modules,venv"`

- `-l`, `--log-level LEVEL`
  Set logging level.
  Choices: `debug`, `info`, `warning`, `error`, `critical`
  Default: `info`

- `--save PATH`
  Save the output to a file.
  Example: `--save output.txt`

- `--detail`
  Print all files found per category in detailed format.

- `-h`, `--help`
  Show help message and exit.
