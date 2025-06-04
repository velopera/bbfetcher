bbfetcher API Documentation
1. Package Overview
The bbfetcher package provides a Python interface for fetching and unpacking Git repositories using BitBake-style URIs. It leverages BitBake's fetch2 module to handle repository operations.

2. Class Reference
2.1 BitBakeFetcher Class
Constructor
python
BitBakeFetcher(download_dir="tmp/bare_repos")
Parameter	Type	Description	Default
download_dir	str	Path where bare repositories will be stored	"tmp/bare_repos"
Initialization Behavior:

Creates specified download directory if it doesn't exist

Initializes internal state for tracking fetched repositories

2.1.1 Methods
fetch(uri)
Fetches a repository using BitBake-style URI.

Signature:

python
def fetch(uri: str) -> str
Parameters:

Parameter	Type	Description
uri	str	BitBake-style repository URI
URI Format:

git://<host>/<path>[;<param>=<value>]*
Supported Parameters:

branch: Branch name

rev: Specific revision (overrides branch)

protocol: Transfer protocol (https, ssh, etc.)

Returns:

Local filesystem path to the downloaded bare repository (str)

Example:

python
path = fetcher.fetch("git://github.com/example/repo.git;branch=main;protocol=https")
unpack(uri, destdir=None)
Unpacks a previously fetched repository to a working directory.

Signature:

python
def unpack(uri: str, destdir: Optional[str] = None) -> str
Parameters:

Parameter	Type	Description
uri	str	Original URI used to fetch repository
destdir	str	Optional destination path	None
Returns:

Path to unpacked repository (str)

Behavior:

Verifies repository was previously fetched

Creates destination directory (removes existing if present)

Clones bare repository without checkout

Checks out specific commit

Example:

python
# Automatic destination
path = fetcher.unpack(uri)

# Custom destination
path = fetcher.unpack(uri, destdir="custom/path")
fetch_and_unpack_all(uris)
Convenience method to process multiple repositories.

Signature:

python
def fetch_and_unpack_all(uris: List[str]) -> List[Tuple[str, str, str]]
Parameters:

Parameter	Type	Description
uris	List[str]	List of BitBake-style URIs
Returns:

List of tuples containing (uri, bare_path, unpacked_path)

Example:

python
results = fetcher.fetch_and_unpack_all([
    "git://repo1.example.com;branch=main",
    "git://repo2.example.com;rev=abc123"
])
2.1.2 Properties
fetched_repos
Dictionary containing metadata about fetched repositories.

Type:

python
Dict[str, Dict[str, Any]]
Structure:

python
{
    "resolved_uri": {
        "fetcher": FetchObject,
        "commit": "abc123",
        "ud": FetchDataObject
    }
}
3. Error Reference
Exception	Cause
ValueError	Invalid URIs or operations on non-fetched repos
subprocess.CalledProcessError	Git command failures
bb.fetch2.FetchError	BitBake fetch operation failures
4. Examples
4.1 Basic Usage
python
from bbfetcher import BitBakeFetcher

# Initialize with custom directory
fetcher = BitBakeFetcher(download_dir="my_downloads")

# Single repo operations
bare_path = fetcher.fetch("git://github.com/example/repo.git")
unpacked_path = fetcher.unpack("git://github.com/example/repo.git")

# Batch processing
results = fetcher.fetch_and_unpack_all([
    "git://repo1.example.com;branch=main",
    "git://repo2.example.com;rev=abc123"
])
4.2 Accessing Metadata
python
repo_data = fetcher.fetched_repos["git://example.com/repo.git"]
commit = repo_data['commit']  # Get resolved commit
5. Requirements
Component	Version
Python	3.9+
Git	2.20+
BitBake	2.0+
