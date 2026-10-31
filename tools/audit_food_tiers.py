#!/usr/bin/env python3
"""靜態核對冷熱設定的 ID、重複項及對應 JAR 物品模型；不執行 Gradle。"""
from __future__ import annotations
import argparse
import collections
import pathlib
import re
import sys
import zipfile

PATTERN = re.compile(r"^([a-z0-9_.-]+):([a-z0-9_./-]+)\s*=\s*(-?[0-9]+)$")

def main() -> int:
    parser = argparse.ArgumentParser(description="飲食冷暖：靜態冷熱設定稽核")
    parser.add_argument("--tiers", type=pathlib.Path, default=pathlib.Path("src/main/resources/food_temperature_tiers.txt"))
    parser.add_argument("--mods", type=pathlib.Path, help="存放模組 JAR 的資料夾（選用）")
    args = parser.parse_args()
    records: dict[str, tuple[int, int]] = {}
    errors = []
    for line_no, raw in enumerate(args.tiers.read_text(encoding="utf-8").splitlines(), 1):
        clean = raw.split("#", 1)[0].strip()
        if not clean:
            continue
        match = PATTERN.fullmatch(clean)
        if not match:
            errors.append(f"第 {line_no} 行：格式錯誤：{clean}")
            continue
        namespace, item, value = match.groups()
        key = f"{namespace}:{item}"
        tier = int(value)
        if not -3 <= tier <= 3:
            errors.append(f"第 {line_no} 行：階級超出 -3..3：{key}={tier}")
        if key in records:
            errors.append(f"第 {line_no} 行：重複 ID {key}（前次在第 {records[key][1]} 行）")
        records[key] = (tier, line_no)
    print(f"冷熱設定總數：{len(records)}")
    print("命名空間分布：")
    for namespace, count in sorted(collections.Counter(x.split(":", 1)[0] for x in records).items()):
        print(f"  {namespace}: {count}")
    if args.mods:
        models = set()
        for jar in sorted(args.mods.glob("*.jar")):
            try:
                with zipfile.ZipFile(jar) as archive:
                    for path in archive.namelist():
                        match = re.fullmatch(r"assets/([^/]+)/models/item/(.+)\.json", path)
                        if match:
                            models.add(f"{match[1]}:{match[2]}")
            except (OSError, zipfile.BadZipFile) as exc:
                errors.append(f"無法讀取 {jar.name}：{exc}")
        for key in records:
            if key not in models:
                print(f"待核對模型（可能為原版物品、缺少 JAR 或非標準模型）：{key}")
        print("注意：模型檢查不能證明物品已註冊、可食用或可觸發食用完成事件。")
    for error in errors:
        print(f"錯誤：{error}", file=sys.stderr)
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
