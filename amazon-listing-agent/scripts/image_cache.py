from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CACHE_ENV = "LISTING_IMAGE_CACHE_PATH"


def default_cache_path() -> Path:
    override = os.environ.get(CACHE_ENV)
    if override:
        return Path(override).expanduser()
    return Path.home() / ".codex" / "shared" / "image-analysis-cache.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_cache(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "entries": {}}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if "entries" not in data or not isinstance(data["entries"], dict):
        data["entries"] = {}
    data.setdefault("version", 1)
    return data


def save_cache(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = now_iso()
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    temp.replace(path)


def fingerprint_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def derive_cache_key(product_id: str, fingerprints: list[str]) -> str:
    if fingerprints:
        source = "|".join(fingerprints)
    elif product_id:
        source = product_id
    else:
        source = now_iso()
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:24]


def parse_facts(value: str) -> dict[str, Any]:
    if not value:
        return {}
    data = json.loads(value)
    if not isinstance(data, dict):
        raise ValueError("--facts-json must be a JSON object")
    return data


def command_path(_: argparse.Namespace) -> int:
    print(default_cache_path())
    return 0


def command_write(args: argparse.Namespace) -> int:
    cache_path = default_cache_path()
    cache = load_cache(cache_path)
    images = [Path(value).expanduser() for value in args.image]
    fingerprints = [fingerprint_file(path) for path in images]
    cache_key = args.cache_key or derive_cache_key(args.product_id or "", fingerprints)
    existing = cache["entries"].get(cache_key, {})
    created_at = existing.get("created_at") or now_iso()
    entry = {
        "cache_key": cache_key,
        "product_id": args.product_id or existing.get("product_id", ""),
        "image_fingerprints": fingerprints or existing.get("image_fingerprints", []),
        "image_paths": [str(path) for path in images] or existing.get("image_paths", []),
        "summary": args.summary,
        "facts": parse_facts(args.facts_json),
        "source_skill": args.source_skill,
        "created_at": created_at,
        "updated_at": now_iso(),
    }
    cache["entries"][cache_key] = entry
    save_cache(cache_path, cache)
    print(json.dumps(entry, ensure_ascii=False, indent=2))
    return 0


def command_read(args: argparse.Namespace) -> int:
    cache = load_cache(default_cache_path())
    entry = cache["entries"].get(args.cache_key)
    if entry is None:
        print(json.dumps({"error": "cache key not found", "cache_key": args.cache_key}, ensure_ascii=False))
        return 1
    print(json.dumps(entry, ensure_ascii=False, indent=2))
    return 0


def command_latest(args: argparse.Namespace) -> int:
    cache = load_cache(default_cache_path())
    entries = list(cache["entries"].values())
    if args.product_id:
        entries = [entry for entry in entries if entry.get("product_id") == args.product_id]
    if not entries:
        print(json.dumps({"error": "no cached image analysis found"}, ensure_ascii=False))
        return 1
    latest = sorted(entries, key=lambda entry: entry.get("updated_at", ""), reverse=True)[0]
    print(json.dumps(latest, ensure_ascii=False, indent=2))
    return 0


def command_list(args: argparse.Namespace) -> int:
    cache = load_cache(default_cache_path())
    entries = list(cache["entries"].values())
    if args.product_id:
        entries = [entry for entry in entries if entry.get("product_id") == args.product_id]
    compact = [
        {
            "cache_key": entry.get("cache_key"),
            "product_id": entry.get("product_id"),
            "summary": entry.get("summary", "")[:120],
            "updated_at": entry.get("updated_at"),
        }
        for entry in sorted(entries, key=lambda item: item.get("updated_at", ""), reverse=True)
    ]
    print(json.dumps(compact, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Shared image analysis cache for Amazon Listing skills.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    path_parser = subparsers.add_parser("path", help="Print the active cache file path.")
    path_parser.set_defaults(func=command_path)

    write_parser = subparsers.add_parser("write", help="Write one image analysis snapshot.")
    write_parser.add_argument("--cache-key", default="")
    write_parser.add_argument("--product-id", default="")
    write_parser.add_argument("--image", action="append", default=[])
    write_parser.add_argument("--summary", required=True)
    write_parser.add_argument("--facts-json", default="{}")
    write_parser.add_argument("--source-skill", default="amazon-listing-agent")
    write_parser.set_defaults(func=command_write)

    read_parser = subparsers.add_parser("read", help="Read one cache entry by cache key.")
    read_parser.add_argument("--cache-key", required=True)
    read_parser.set_defaults(func=command_read)

    latest_parser = subparsers.add_parser("latest", help="Read the latest cache entry.")
    latest_parser.add_argument("--product-id", default="")
    latest_parser.set_defaults(func=command_latest)

    list_parser = subparsers.add_parser("list", help="List cached image analysis entries.")
    list_parser.add_argument("--product-id", default="")
    list_parser.set_defaults(func=command_list)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
