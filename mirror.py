# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "tomli>=2.2.1",
#     "tomli-w>=1.2.0",
#     "urllib3>=2",
#     "packaging>=21.0",
# ]
# ///

import subprocess
from pathlib import Path

import tomli
import tomli_w
import urllib3
from packaging.requirements import Requirement
from packaging.version import Version


def main():
    # Load pyproject.toml
    with open(Path(__file__).parent / "pyproject.toml", "rb") as f:
        pyproject = tomli.load(f)
    # Load README.md
    with open(Path(__file__).parent / "README.md", "r") as f:
        readme = f.read()

    # 获取当前版本的 yamlfmt
    deps = pyproject["project"]["dependencies"]
    assert len(deps) == 1
    yamlfmt_dep = Requirement(deps[0])
    assert yamlfmt_dep.name == "google-yamlfmt"
    yamlfmt_specs = list(yamlfmt_dep.specifier)
    assert len(yamlfmt_specs) == 1
    assert yamlfmt_specs[0].operator == "=="
    current_version = Version(yamlfmt_specs[0].version)

    # Get yamlfmt versions from PyPI
    http = urllib3.PoolManager()
    resp = http.request("GET", "https://pypi.org/pypi/google-yamlfmt/json")
    if resp.status != 200:
        raise RuntimeError("Failed to fetch data from PyPI")

    versions = [Version(release) for release in resp.json()["releases"]]
    versions = [v for v in versions if v > current_version and not v.is_prerelease]
    versions.sort()

    # Update yamlfmt for each version
    for version in versions:
        # Update pyproject.toml
        pyproject["project"]["version"] = str(version)
        pyproject["project"]["dependencies"] = [f"google-yamlfmt=={version}"]
        # Update README.md
        updated_readme = readme.replace(str(current_version), str(version))

        # Write pyproject.toml and README.md
        with open(Path(__file__).parent / "pyproject.toml", "wb") as f:
            tomli_w.dump(pyproject, f)
        with open(Path(__file__).parent / "README.md", "w") as f:
            f.write(updated_readme)

        # Commit and tag
        subprocess.run(["git", "add", "pyproject.toml", "README.md"])
        subprocess.run(
            ["git", "commit", "-m", f":arrow_up: bump typos version to {version}"]
        )
        subprocess.run(["git", "tag", f"v{version}"])


if __name__ == "__main__":
    main()
