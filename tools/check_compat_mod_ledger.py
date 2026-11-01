#!/usr/bin/env python3
"""核對每個兼容模組的永久審查台帳與目前執行設定是否一致。"""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path("src/main/resources")
LEDGER = Path("compatibility/compat_mod_review_status.csv")
REVIEW = Path("compatibility/neutral_hydration_review.csv")
THIRST = ROOT / "data/toughasnails/tags/item/thirst"
ERRORS = []

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def main():
    tiers = Counter()
    for raw in (ROOT / "food_temperature_tiers.txt").read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            item = line.split("=", 1)[0].strip()
            tiers[item.split(":", 1)[0]] += 1
    hydration = Counter()
    for path in sorted(THIRST.glob("*_thirst_drinks.json")):
        for entry in json.loads(path.read_text(encoding="utf-8"))["values"]:
            hydration[entry["id"].split(":", 1)[0]] += 1
    review = Counter(row["物品 ID"].split(":", 1)[0] for row in read_csv(REVIEW))
    ledger = read_csv(LEDGER)
    ids = [row["modid"] for row in ledger]
    if len(ids) != len(set(ids)):
        ERRORS.append("兼容模組台帳存在重複 modid")
    for mod in sorted(set(tiers) | set(hydration) | set(review)):
        if mod not in ids:
            ERRORS.append(f"台帳缺少命名空間：{mod}")
    for row in ledger:
        mod = row["modid"]
        for key, actual in (
            ("冷熱設定筆數", tiers[mod]),
            ("補水設定筆數", hydration[mod]),
            ("已列入審查表筆數", review[mod]),
        ):
            try:
                recorded = int(row[key])
            except (ValueError, TypeError):
                ERRORS.append(f"{mod} 的 {key} 不是整數")
                continue
            if recorded != actual:
                ERRORS.append(f"{mod} 的 {key} 台帳 {recorded}／實際 {actual}")
        try:
            verified = int(row["可食用性已核對數（保守估計）"])
            if verified < 0 or verified > max(tiers[mod] + review[mod], hydration[mod]):
                ERRORS.append(f"{mod} 可食用性已核對數異常：{verified}")
        except (ValueError, TypeError):
            ERRORS.append(f"{mod} 可食用性已核對數不是整數")
    print(f"兼容模組台帳 {len(ledger)} 筆；冷熱 {sum(tiers.values())} 筆；補水 {sum(hydration.values())} 筆；錯誤 {len(ERRORS)} 筆")
    for error in ERRORS:
        print("錯誤：" + error)
    return bool(ERRORS)

if __name__ == "__main__":
    raise SystemExit(main())
