import os
import sys
import shutil
import subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bb.fetch2 import Fetch, get_srcrev

class DummyData:
    def __init__(self):
        self.vars = {}

    def getVar(self, var, inherit=False):
        return self.vars.get(var)

    def setVar(self, var, val):
        self.vars[var] = val

    def delVar(self, var):
        if var in self.vars:
            del self.vars[var]

    def createCopy(self):
        copy = DummyData()
        copy.vars = self.vars.copy()
        return copy

    def expand(self, s):
        return s

class BitBakeFetcher:
    def __init__(self, download_dir="/tmp/bare_repos"):
        self.d = DummyData()
        self.d.setVar('DL_DIR', download_dir)
        self.d.setVar('BB_NO_NETWORK', '0')
        os.makedirs(download_dir, exist_ok=True)

    def fetch(self, uri):
        self.uri = uri
        rev = 'main'
        if ';rev=' in uri:
            rev = uri.split(';rev=')[1].split(';')[0]

        url_base = uri.split(';')[0]
        self.d.setVar('SRCREV_default', rev)
        src_uri = ';'.join([p for p in uri.split(';') if not p.startswith('rev=')])
        self.d.setVar('SRC_URI', src_uri)

        commit = get_srcrev(self.d)
        uri = uri.replace(f";rev={rev}", f";rev={commit}")

        self.fetcher = Fetch([uri], self.d)
        self.fetcher.download()

        self.commit = self.fetcher.ud[uri].revision
        return self.fetcher.localpath(uri)
    
    def unpack(self, uri=None, destdir=None):
        if uri is None:
            uri = self.uri
        ud = self.fetcher.ud[uri]
        bare_repo_path = ud.localpath
        rev = self.commit or "HEAD"

        # Extract repo name from path
        repo_name = os.path.splitext(os.path.basename(ud.host + ud.path))[0]
        if destdir is None:
            destdir = os.path.join("tmp/unpacked_repos", repo_name)

        destdir = os.path.abspath(destdir)

        if os.path.exists(destdir):
            shutil.rmtree(destdir)
        os.makedirs(os.path.dirname(destdir), exist_ok=True)

        subprocess.run(["git", "clone", "--no-checkout", bare_repo_path, destdir], check=True)
        subprocess.run(["git", "checkout", rev], cwd=destdir, check=True)

        print(f"✅ Unpacked to: {destdir}")
        return destdir


# Example usage
if __name__ == "__main__":
    fetcher = BitBakeFetcher()
    local_path = fetcher.fetch("git://github.com/SecOPERA-toffy/toffy-oatpp.git;branch=main;protocol=https")
    print(f"Downloaded to: {local_path}")