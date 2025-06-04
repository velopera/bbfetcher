import os
import sys
import shutil
import subprocess
from typing import List, Tuple, Optional, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bb.fetch2 import Fetch, get_srcrev, FetchError

class DummyData:
    def __init__(self):
        self.vars = {}

    def getVar(self, var: str, inherit: bool = False) -> Optional[str]:
        return self.vars.get(var)

    def setVar(self, var: str, val: str) -> None:
        self.vars[var] = val

    def delVar(self, var: str) -> None:
        if var in self.vars:
            del self.vars[var]

    def createCopy(self) -> 'DummyData':
        copy = DummyData()
        copy.vars = self.vars.copy()
        return copy

    def expand(self, s: str) -> str:
        return s

class BitBakeFetcher:
    def __init__(self, download_dir: str = "tmp/bare_repos") -> None:
        self.d = DummyData()
        self.d.setVar('DL_DIR', download_dir)
        self.d.setVar('BB_NO_NETWORK', '0')
        self.d.setVar('SRC_URI', '')
        os.makedirs(download_dir, exist_ok=True)
        self.fetched_repos: Dict[str, Dict[str, Any]] = {}

    def _resolve_branch_fallback(self, uri: str) -> str:
        if 'branch=' not in uri and 'rev=' not in uri:
            return uri + ";branch=main"
        return uri

    def _try_alternative_branches(self, original_uri: str, error: FetchError) -> str:
        if "Unable to resolve" in str(error):
            if "branch=main" in original_uri:
                modified_uri = original_uri.replace("branch=main", "branch=master")
                print(f"⚠️ Trying fallback branch 'master' for {original_uri}")
                try:
                    return self.fetch(modified_uri)
                except FetchError:
                    pass
        raise error

    def fetch(self, uri: str, recursive_depth: int = 0) -> str:
        try:
            # Extract parameters
            params = {p.split('=')[0]: p.split('=')[1] for p in uri.split(';')[1:] if '=' in p}
            rev = params.get('rev')
            branch = params.get('branch')
            
            # Build SRC_URI without rev=
            src_uri = ';'.join([p for p in uri.split(';') if not p.startswith('rev=')])
            self.d.setVar('SRC_URI', src_uri)
            
            # Handle revision
            if rev:
                self.d.setVar('SRCREV_default', rev)
            else:
                # If branch is specified and no rev, attempt to resolve it
                if branch:
                    self.d.setVar('SRCREV_default', branch)
                else:
                    self.d.setVar('SRCREV_default', 'main')  # Fallback default

            try:
                commit = get_srcrev(self.d)
            except Exception as e:
                if "recursive references" in str(e):
                    if recursive_depth > 1:
                        raise FetchError("Too many recursive reference attempts")
                    print(f"⚠️ Recursive reference detected, cleaning up and retrying (depth {recursive_depth})")
                    self.d.delVar('SRC_URI')
                    self.d.setVar('SRC_URI', '')
                    return self.fetch(uri, recursive_depth=recursive_depth + 1)
                raise

            resolved_uri = uri.replace(f";rev={rev}", f";rev={commit}")

            fetcher = Fetch([resolved_uri], self.d)
            fetcher.download()

            self.fetched_repos[resolved_uri] = {
                'fetcher': fetcher,
                'commit': fetcher.ud[resolved_uri].revision,
                'ud': fetcher.ud[resolved_uri],
                'original_uri': uri
            }

            return fetcher.localpath(resolved_uri)

        except FetchError as e:
            return self._try_alternative_branches(uri, e)

    def unpack(self, uri: str, destdir: Optional[str] = None) -> str:
        resolved_uri = next(
            (k for k, v in self.fetched_repos.items() if v.get('original_uri') == uri),
            uri
        )

        if resolved_uri not in self.fetched_repos:
            raise ValueError(f"URI '{uri}' has not been fetched yet!")

        repo_data = self.fetched_repos[resolved_uri]
        ud = repo_data['ud']
        rev = repo_data['commit']
        bare_repo_path = ud.localpath

        original_uri = repo_data.get('original_uri', uri)
        repo_name = os.path.splitext(os.path.basename(
            original_uri.split(';')[0].replace('git://', '')
        ))[0]

        if destdir is None:
            destdir = os.path.join("tmp/unpacked_repos", repo_name)

        destdir = os.path.abspath(destdir)

        if os.path.exists(destdir):
            shutil.rmtree(destdir)
        os.makedirs(os.path.dirname(destdir), exist_ok=True)

        try:
            subprocess.run(
                ["git", "clone", "--no-checkout", bare_repo_path, destdir],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            subprocess.run(
                ["git", "checkout", rev],
                cwd=destdir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        except subprocess.CalledProcessError as e:
            shutil.rmtree(destdir, ignore_errors=True)
            error_msg = e.stderr if isinstance(e.stderr, str) else e.stderr.decode()
            raise RuntimeError(f"Failed to unpack repository: {error_msg.strip()}")

        print(f"✅ Unpacked to: {destdir}")
        return destdir

    def fetch_and_unpack_all(self, uris: List[str]) -> List[Tuple[str, str, str]]:
        results = []
        for uri in uris:
            try:
                print(f"💽 Fetching: {uri}")
                path = self.fetch(uri)
                print(f"📦 Unpacking: {uri}")
                unpacked_path = self.unpack(uri=uri)
                results.append((uri, path, unpacked_path))
            except Exception as e:
                print(f"❌ Failed to fetch/unpack {uri}: {str(e)}")
        return results

if __name__ == "__main__":
    fetcher = BitBakeFetcher()
    local_path = fetcher.fetch("git://github.com/SecOPERA-toffy/toffy-oatpp.git;branch=main;protocol=https")
    print(f"Downloaded to: {local_path}")
