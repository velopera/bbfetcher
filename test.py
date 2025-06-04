from fetcher import BitBakeFetcher

fetcher = BitBakeFetcher()
path = fetcher.fetch("git://github.com/SecOPERA-toffy/toffy-oatpp.git;branch=main;protocol=https")
fetcher.unpack()