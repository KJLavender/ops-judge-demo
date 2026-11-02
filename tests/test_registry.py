"""Simulates a dependency registry that is briefly unreachable.

When the file `demo/registry-outage` exists, the first attempt of a CI run fails the way a real DNS outage
does; a rerun (attempt 2+) passes. This is the kind of failure a rerun should fix.
"""

import os
import pathlib


def test_fetch_package_index():
    outage = pathlib.Path("demo/registry-outage").exists()
    if outage and os.environ.get("GITHUB_RUN_ATTEMPT", "1") == "1":
        raise ConnectionError(
            "HTTPSConnectionPool(host='registry.example.org', port=443): Max retries exceeded "
            "(Caused by NameResolutionError: Failed to resolve 'registry.example.org' "
            "([Errno -3] Temporary failure in name resolution))"
        )
