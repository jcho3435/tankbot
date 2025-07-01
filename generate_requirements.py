"""
This script is used to generate requirements.txt. It is necessary to run this
instead of running pipreqs directly due to bugs with pipreqs mapping.

Make sure venv is active before running.
"""

import subprocess
from pathlib import Path

import re
from packaging.version import parse as parse_version

def deduplicate_requirements(lines): # ty chatgpt
    """
    Keep only the latest version per package.
    Preserve lines that don't match 'pkg==ver' format as-is.
    """
    pkg_versions = {}
    others = []

    # regex to parse lines like: pkg==ver
    pattern = re.compile(r"^([a-zA-Z0-9_\-]+)==(.+)$")

    for line in lines:
        m = pattern.match(line)
        if m:
            pkg, ver = m.group(1).lower(), m.group(2)
            # Update only if this version is newer
            if pkg not in pkg_versions or parse_version(ver) > parse_version(pkg_versions[pkg]):
                pkg_versions[pkg] = ver
        else:
            others.append(line)

    # Rebuild lines with latest versions
    deduped = [f"{pkg}=={ver}" for pkg, ver in sorted(pkg_versions.items())]
    deduped.extend(others)
    return deduped

#constants
REQUIREMENTS_FILE = Path("requirements.txt")
CUSTOM_LINE = (
    "discord-ext-fancy-help @ git+https://github.com/redParrot17/discord-ext-fancy-help@07bd395b9570d621c851a8adc38ee05db24602b5"
)

# run pipreqs
print("Running pipreqs")
subprocess.run(
    ["pipreqs", "--force"],
    check=True
)

# deduplicate lines
if REQUIREMENTS_FILE.exists():
    print("Deduplicating requirements.txt")
    with REQUIREMENTS_FILE.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    unique_lines = deduplicate_requirements(lines)

    #append custom package if not already present
    if CUSTOM_LINE not in unique_lines:
        unique_lines.append(CUSTOM_LINE)

    with REQUIREMENTS_FILE.open("w", encoding="utf-8") as f:
        f.write("\n".join(unique_lines) + "\n")

    print("requirements.txt updated")
else:
    print("requirements.txt missing???")