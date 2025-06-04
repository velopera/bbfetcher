from fetcher import BitBakeFetcher
import shutil
import os

def test_single_repo():
    print("=== Testing single repository fetch and unpack ===")
    try:
        fetcher = BitBakeFetcher(download_dir="test_downloads")
        
        # Test fetch
        uri = "git://github.com/SecOPERA-toffy/toffy-oatpp.git;branch=main;protocol=https"
        print(f"Fetching repository: {uri}")
        path = fetcher.fetch(uri)
        print(f"✅ Repository downloaded to: {path}")
        
        # Test unpack with automatic destination
        print("\nUnpacking repository...")
        unpacked_path = fetcher.unpack(uri)
        print(f"✅ Repository unpacked to: {unpacked_path}")
        
        # Verify contents
        if os.path.exists(os.path.join(unpacked_path, ".git")):
            print("✅ .git directory found - unpack successful")
        else:
            print("❌ .git directory missing - unpack failed")
            
        return True
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    finally:
        # Cleanup
        if 'fetcher' in locals():
            if os.path.exists("test_downloads"):
                shutil.rmtree("test_downloads")
            if os.path.exists("tmp/unpacked_repos"):
                shutil.rmtree("tmp/unpacked_repos")

def test_multiple_repos():
    print("\n=== Testing multiple repository fetch and unpack ===")
    try:
        fetcher = BitBakeFetcher(download_dir="test_downloads")
        
        test_repos = [
            "git://github.com/SecOPERA-toffy/toffy-oatpp.git;branch=main;protocol=https",
            "git://github.com/SecOPERA-toffy/oatpp.git;branch=master;protocol=https",
            "git://github.com/SecOPERA-toffy/oatpp-socketio.git;branch=main;protocol=https"
        ]
        
        print("Fetching and unpacking multiple repositories...")
        results = fetcher.fetch_and_unpack_all(test_repos)
        
        print("\nResults:")
        for uri, bare_path, unpacked_path in results:
            print(f"\nRepository: {uri}")
            print(f"Bare repo: {bare_path}")
            print(f"Unpacked to: {unpacked_path}")
            
            # Verify unpack
            if os.path.exists(unpacked_path):
                print("✅ Unpack verified")
            else:
                print("❌ Unpack failed")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    finally:
        # Cleanup
        if 'fetcher' in locals():
            if os.path.exists("test_downloads"):
                shutil.rmtree("test_downloads")
            if os.path.exists("tmp/unpacked_repos"):
                shutil.rmtree("tmp/unpacked_repos")

def test_error_handling():
    print("\n=== Testing error handling ===")
    tests = [
        {
            "name": "Invalid URI format",
            "uri": "invalid_uri_format",
            "should_fail": True
        },
        {
            "name": "Non-existent repository",
            "uri": "git://github.com/nonexistent/repo.git;branch=main",
            "should_fail": True
        },
        {
            "name": "Unpack before fetch",
            "uri": "git://github.com/SecOPERA-toffy/toffy-oatpp.git",
            "should_fail": True,
            "operation": "unpack"
        }
    ]

    all_passed = True  # ← track overall result

    for test in tests:
        print(f"\nTest: {test['name']}")
        try:
            fetcher = BitBakeFetcher()

            if test.get("operation", "fetch") == "fetch":
                fetcher.fetch(test["uri"])
            else:
                fetcher.unpack(test["uri"])

            if test["should_fail"]:
                print("❌ Test failed - expected error but none raised")
                all_passed = False
            else:
                print("✅ Test passed")
        except Exception as e:
            if test["should_fail"]:
                print(f"✅ Test passed (expected error: {str(e)})")
            else:
                print(f"❌ Test failed (unexpected error: {str(e)})")
                all_passed = False
        finally:
            if 'fetcher' in locals():
                if os.path.exists("tmp/bare_repos"):
                    shutil.rmtree("tmp/bare_repos")
                if os.path.exists("tmp/unpacked_repos"):
                    shutil.rmtree("tmp/unpacked_repos")

    return all_passed

if __name__ == "__main__":
    print("Starting bbfetcher tests...\n")
    
    # Run tests
    single_repo_success = test_single_repo()
    multi_repo_success = test_multiple_repos()
    error_handling_success = test_error_handling()
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Single repo test: {'PASSED' if single_repo_success else 'FAILED'}")
    print(f"Multiple repos test: {'PASSED' if multi_repo_success else 'FAILED'}")
    print(f"Error handling test: {'PASSED' if error_handling_success else 'FAILED'}")
    
    if all([single_repo_success, multi_repo_success, error_handling_success]):
        print("\n✅ All tests passed successfully!")
    else:
        print("\n❌ Some tests failed")