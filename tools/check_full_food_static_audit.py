#!/usr/bin/env python3
"""稽核大批次靜態審查表與執行設定及官方來源候選庫的一致性。"""
import csv
import json
from pathlib import Path

ROOT = Path("src/main/resources")
AUDIT = Path("compatibility/full_food_static_audit_2026-11-02.csv")
SOURCE = Path("compatibility/extradelight_source_food_inventory_1_21.csv")
PROGRESS = Path("compatibility/food_item_progress.csv")
REVIEW = Path("compatibility/neutral_hydration_review.csv")
CANDIDATE = Path("compatibility/untagged_liquid_food_candidates.csv")


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main():
    errors = []
    temperature = {}
    for line in (ROOT / "food_temperature_tiers.txt").read_text(encoding="utf-8").splitlines():
        clean = line.split("#", 1)[0].strip()
        if clean:
            key, value = clean.split("=", 1)
            temperature[key.strip()] = float(value.strip())

    progress = {row["物品 ID"] for row in read_csv(PROGRESS)}
    review = {row["物品 ID"] for row in read_csv(REVIEW)}
    candidate = {row["物品 ID"] for row in read_csv(CANDIDATE)}
    source = {row["物品 ID"] for row in read_csv(SOURCE)}
    thirst, hydration = {}, {}
    root = ROOT / "data/toughasnails/tags/item"
    for category, levels, out in (
        ("thirst", (1, 2, 3, 4, 6), thirst),
        ("hydration", (10, 20, 30, 50), hydration),
    ):
        for level in levels:
            path = root / category / f"{level}_{category}_drinks.json"
            for entry in json.loads(path.read_text(encoding="utf-8"))["values"]:
                item = entry["id"]
                if item in out:
                    errors.append(f"跨級別重複 {category}：{item}")
                out[item] = level

    tracked = set(temperature) | progress | review | candidate | set(hydration)
    expected = tracked | source
    rows = read_csv(AUDIT)
    audit_ids = [row["物品 ID"] for row in rows]
    if len(audit_ids) != len(set(audit_ids)):
        errors.append("靜態審查表存在重複 ID")
    actual = set(audit_ids)
    for item in sorted(expected - actual):
        errors.append(f"大批次審查表缺少：{item}")
    for item in sorted(actual - expected):
        errors.append(f"大批次審查表多出無來源 ID：{item}")
    for row in rows:
        item = row["物品 ID"]
        v = row["已有冷熱設定值"].strip()
        if item in temperature:
            if not v or float(v) != temperature[item]:
                errors.append(f"冷熱數值與審查表不符：{item}")
        elif v:
            errors.append(f"審查表聲稱冷熱設定，但目前設定檔沒有：{item}")
        for field, groups in (
            ("TAN 口渴標籤階級", thirst),
            ("TAN 補水標籤階級", hydration),
        ):
            found = row[field].strip()
            expected_level = str(groups[item]) if item in groups else ""
            if found != expected_level:
                errors.append(f"審查表級別不符：{item} / {field}")
        expected_origin = "專案既有追蹤" if item in tracked else "Extra Delight 官方來源新候選"
        if row["候選來源"] != expected_origin:
            errors.append(f"候選來源不符：{item}")
    print(
        f"大批次初篩 {len(rows)} 項；原既有／目前追蹤 {len(tracked)} 項；"
        f"Extra Delight 來源 {len(source)} 項；"
        f"非零冷熱 {len(temperature)} 項；補水 {len(hydration)} 項；"
        f"錯誤 {len(errors)} 筆"
    )
    for e in errors[:100]:
        print("錯誤：" + e)
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
