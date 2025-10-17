#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Merge current directory into HOME safely."
    )
    parser.add_argument("--dry-run", action="store_true", help="Echo only, do not perform merge")
    parser.add_argument("--verbose", action="store_true", help="Show details")
    args = parser.parse_args()

    dry_run = args.dry_run
    verbose = args.verbose

    src_dir = Path.cwd()
    home_dir = Path(os.environ.get("HOME", "/root"))

    if src_dir.resolve() == home_dir.resolve():
        print(f"Error: Current dir is HOME ({home_dir})", file=sys.stderr)
        sys.exit(1)

    items = [p.relative_to(src_dir) for p in src_dir.rglob("*")]

    if not items:
        print("No files or directories found in current directory. Nothing to merge.")
        sys.exit(0)

    conflicts = []
    for rel_path in items:
        dest_path = home_dir / rel_path
        if dest_path.exists():
            conflicts.append(str(rel_path))
            if verbose:
                print(f"Conflict detected: {rel_path}")

    if conflicts:
        print(f"\nERROR: Detected {len(conflicts)} conflict(s) in target HOME. Merge aborted. No changes applied.")
        print("Conflicting paths (relative to HOME):")
        for c in conflicts:
            print(f"  - {c}")
        print("\nTo proceed, resolve or remove the conflicting items in your HOME, then re-run this script.")
        sys.exit(2)

    if dry_run:
        print("Dry run: no files will be copied.")
    else:
        print("No conflicts detected. Ready to merge.")

if __name__ == "__main__":
    main()

