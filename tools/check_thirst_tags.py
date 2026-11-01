#!/usr/bin/env python3
"""稽核 TAN 10.1.0.13 補水標籤：ID、重複、冷熱設定來源與可選模組。"""
import json
import csv
import re
from pathlib import Path

ROOT = Path("src/main/resources/data/toughasnails/tags/item")
TIERS = Path("src/main/resources/food_temperature_tiers.txt")
PATTERN = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
GROUPS = {
    "soup": (("thirst/2_thirst_drinks.json", "hydration/30_hydration_drinks.json")),
    "drink": (("thirst/4_thirst_drinks.json", "hydration/50_hydration_drinks.json")),
    "dessert": (("thirst/1_thirst_drinks.json", "hydration/10_hydration_drinks.json")),
}

def main():
    known = {line.split("=", 1)[0].strip() for line in TIERS.read_text(encoding="utf-8").splitlines() if "=" in line and not line.lstrip().startswith("#")}
    errors = []
    # 補水不依賴冷熱值；允許 CSV 中明確記錄的中性料理。
    with Path("compatibility/food_item_progress.csv").open(encoding="utf-8-sig", newline="") as handle:
        progress = {row["物品 ID"].strip(): row for row in csv.DictReader(handle)}
    known |= set(progress)
    all_ids = set()
    for group, paths in GROUPS.items():
        members = []
        for rel in paths:
            path = ROOT / rel
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("replace") is not False:
                errors.append(f"{path}: replace 必須為 false")
            ids = []
            for entry in data["values"]:
                if not isinstance(entry, dict) or entry.get("required") is not False:
                    errors.append(f"{path}: 選用模組條目必須 required=false: {entry}")
                    continue
                item = entry.get("id", "")
                if not PATTERN.fullmatch(item) or item not in known:
                    errors.append(f"{path}: ID 不存在於冷熱設定／中性食物進度表或格式錯誤：{item}")
                if item in ids:
                    errors.append(f"{path}: 重複 ID：{item}")
                ids.append(item)
            members.append(set(ids))
        if members[0] != members[1]:
            errors.append(f"{group}: thirst 與 hydration 物品不一致")
        overlap = all_ids & members[0]
        if overlap:
            errors.append(f"{group}: 跨分類重複：{sorted(overlap)}")
        all_ids |= members[0]
        print(f"{group}: {len(members[0])} 個補水物品")
    print(f"補水設定總計 {len(all_ids)} 個物品；錯誤 {len(errors)} 筆")
    for error in errors:
        print("錯誤：" + error)
    return int(bool(errors))

if __name__ == "__main__":
    raise SystemExit(main())
