# bbfetcher
bbfetcher is a Python [API](https://github.com/velopera/bbfetcher/blob/main/API.md) for fetching and unpacking Git repositories using BitBake-style URIs.
It wraps BitBake's internal fetch2 modules to provide an easy way to fetch source code archives or Git repos without manual git cloning.

---
## Features
- Fetch Git repositories using BitBake SRC_URI style URLs
- Automatically resolve revisions and branches
- Support for multiple repositories in one operation
- Downloads to a configurable directory
- Unpacks bare Git repositories to a local directory with proper checkout
- Tracks fetched repositories and their metadata
- Minimal external dependencies

---

## Requirements
Python 3.9 or higher
Git (for repository operations)

## Installation
```bash
git clone https://github.com/velopera/bbfetcher.git
cd bbfetcher
pip install .
```
or directly from the repository directory:

```bash
python setup.py install
```
Basic Usage
```python
from bbfetcher import BitBakeFetcher

# Initialize fetcher with custom download directory
fetcher = BitBakeFetcher(download_dir="tmp/bare_repos")

# Fetch a single repository
local_path = fetcher.fetch("git://github.com/SecOPERA-toffy/toffy-oatpp.git;branch=main;protocol=https")

# Unpack to specific directory
unpacked_path = fetcher.unpack(uri="git://github.com/SecOPERA-toffy/toffy-oatpp.git;branch=main;protocol=https", 
                              destdir="custom/destination")

# Process multiple repositories at once
uris = [
    "git://github.com/example/repo1.git;branch=main",
    "git://github.com/example/repo2.git;rev=abc123"
]
results = fetcher.fetch_and_unpack_all(uris)
```

## Advanced Features
### Repository Tracking
The fetcher maintains state of all fetched repositories including:

- Original URI

- Resolved commit

- Local paths

### Automatic Revision Resolution
When a branch is specified but no revision, the latest commit is automatically resolved.

### Custom Destination Paths
You can specify exact unpack locations or let the fetcher generate them automatically.

## Project Structure
- bbfetcher/
`
- fetcher.py: Main fetcher class implementation

- __init__.py: Package exports

- test.py: Example usage script

- setup.py: Package installation configuration

## Error Handling
The fetcher provides clear error messages for:

- Invalid URIs

- Network failures

- Repository resolution issues

- Destination directory conflicts

## License
This project is licensed under the GNU General Public License version 2.0 (GPL-2.0-only), consistent with the BitBake project it uses.

See the LICENSE file for more details.
