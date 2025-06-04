# bbfetcher

`bbfetcher` is a Python API for fetching and unpacking Git repositories using BitBake-style URIs.  
It wraps BitBake's internal fetch2 modules to provide an easy way to fetch source code archives or Git repos without manual git cloning.

---

## Features

- Fetch Git repositories using BitBake SRC_URI style URLs.
- Automatically resolve revisions and branches.
- Downloads to a configurable directory.
- Unpacks bare Git repositories to a local directory.
- Minimal external dependencies.

## Requirements

- Python 3.9 or higher.

---

## Getting Started

Clone or download this repository and import the `BitBakeFetcher` class in your Python project.

or under this repository directory:

```bash
pip install .
```

### Example

```python
from bbfetcher import BitBakeFetcher

# Initialize fetcher with download directory
fetcher = BitBakeFetcher(download_dir="downloads/")

# Fetch the Git repository, resolving branch and revision automatically
local_path = fetcher.fetch("git://github.com/SecOPERA-toffy/toffy-oatpp.git;branch=main;protocol=https")

print(f"Downloaded bare repository to: {local_path}")

# Unpack the bare repo into a usable source directory
fetcher.unpack(destdir="unpacked/toffy-oatpp")

print("Repository unpacked to 'unpacked/toffy-oatpp'")
```

### Test

```bash
python3 test.py
```
---

## Usage Notes
- The fetch method downloads the bare Git repository into the specified download directory.

- The unpack method checks out the correct commit into the specified destination directory without cloning again.

- The revision used is automatically resolved from the provided URI or defaults to main branch.

- Designed primarily for BitBake-style source fetching workflows but can be adapted for other use cases.

## Project Structure
- bbfetcher/fetcher.py: Main fetcher class wrapping BitBake fetch2 functionality.

- bbfetcher/__init__.py: Module export for easy import.

- main.py: Example script demonstrating usage.

- requirements.txt: Python dependencies (currently minimal).


## License

This project is licensed under the GNU General Public License version 2.0 (GPL-2.0-only), consistent with the BitBake project it uses.

See the LICENSE file for more details.
