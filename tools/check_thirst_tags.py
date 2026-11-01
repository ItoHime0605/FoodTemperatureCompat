#!/usr/bin/env python3
"""稽核 TAN 10.1.0.13 補水標籤：ID、重複、冷熱設定來源與可選模組。"""
import json
import csv
import re
import argparse
import zipfile
from pathlib import Path

ROOT = Path("src/main/resources/data/toughasnails/tags/item")
TIERS = Path("src/main/resources/food_temperature_tiers.txt")
PATTERN = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
GROUPS = {
    "soup": (("thirst/2_thirst_drinks.json", "hydration/30_hydration_drinks.json")),
    "drink": (("thirst/4_thirst_drinks.json", "hydration/50_hydration_drinks.json")),
    "dessert": (("thirst/1_thirst_drinks.json", "hydration/10_hydration_drinks.json")),
    "neutral_salad": (("thirst/3_thirst_drinks.json", "hydration/20_hydration_drinks.json")),
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tan-jar", type=Path, help="選填：Tough As Nails 原始 JAR，檢查原生補水標籤重疊")
    args = parser.parse_args()
    known = {line.split("=", 1)[0].strip() for line in TIERS.read_text(encoding="utf-8").splitlines() if "=" in line and not line.lstrip().startswith("#")}
    errors = []
    # 補水不依賴冷熱值；允許 CSV 中明確記錄的中性料理。
    with Path("compatibility/food_item_progress.csv").open(encoding="utf-8-sig", newline="") as handle:
        progress = {row["物品 ID"].strip(): row for row in csv.DictReader(handle)}
    known |= set(progress)
    review_path = Path("compatibility/neutral_hydration_review.csv")
    with review_path.open(encoding="utf-8-sig", newline="") as handle:
        reviewed = list(csv.DictReader(handle))
    review_ids = [row["物品 ID"].strip() for row in reviewed]
    if len(review_ids) != len(set(review_ids)):
        errors.append("中性補水審查表存在重複物品 ID")
    for item in review_ids:
        if not PATTERN.fullmatch(item):
            errors.append(f"中性補水審查表 ID 格式錯誤：{item}")
    # 審查候選不等於已核准：待確認物品不得僅憑 CSV 存在就通過檢查。
    review_by_id = {row["物品 ID"].strip(): row for row in reviewed}
    allowed_review_ids = {
        item for item, row in review_by_id.items()
        if row["補水判定"] == "已設定少量補水"
        and row["可食用性驗證"] not in ("", "待驗證")
    }
    known |= allowed_review_ids
    all_ids = set()
    assigned_groups = {}
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
        for item in members[0]:
            assigned_groups[item] = group
        print(f"{group}: {len(members[0])} 個補水物品")
    for row in reviewed:
        item = row["物品 ID"].strip()
        if row["補水判定"] == "已設定少量補水":
            if item not in allowed_review_ids:
                errors.append(f"中性食物已補水但缺少可食用性確認：{item}")
            if item not in all_ids:
                errors.append(f"中性食物標記已補水但缺少標籤：{item}")
            elif assigned_groups.get(item) != "neutral_salad":
                errors.append(f"中性食物應使用獨立補水分類：{item} ({assigned_groups.get(item)})")
        if row["補水判定"] == "待確認" and item in all_ids:
            errors.append(f"中性食物尚未完成確認卻已加入補水標籤：{item}")
        if row["補水判定"] == "暫不補水" and item in all_ids:
            errors.append(f"中性補水審查表標記暫不補水，但已被補水標籤包含：{item}")
    print(f"中性／未分類補水審查 {len(review_ids)} 筆")
    # 審查表應與已知冷熱設定分離；明確標記中性者不得同時有非零冷熱值。
    for row in reviewed:
        item = row["物品 ID"].strip()
        if row["溫度分類"] == "中性" and item in {line.split("=", 1)[0].strip() for line in TIERS.read_text(encoding="utf-8").splitlines() if "=" in line and not line.lstrip().startswith("#")}:
            errors.append(f"中性食物意外出現在冷熱設定表：{item}")
    native = set()
    if args.tan_jar:
        # 展開 TAN 原生標籤的 #巢狀參照，避免僅比對直接列出的物品而漏報。
        with zipfile.ZipFile(args.tan_jar) as jar:
            prefix = "data/toughasnails/tags/item/"
            tags = {}
            for filename in jar.namelist():
                if not filename.startswith(prefix) or not filename.endswith(".json"):
                    continue
                key = "toughasnails:" + filename[len(prefix):-5]
                tags[key] = json.loads(jar.read(filename)).get("values", [])
            def expand(tag, seen):
                if tag in seen:
                    errors.append(f"TAN 原生標籤循環參照：{tag}")
                    return set()
                result = set()
                for entry in tags.get(tag, []):
                    item = entry if isinstance(entry, str) else entry.get("id", "")
                    if item.startswith("#"):
                        result |= expand(item[1:], seen | {tag})
                    elif PATTERN.fullmatch(item):
                        result.add(item)
                return result
            for tag in tags:
                if tag.startswith("toughasnails:thirst/") or tag.startswith("toughasnails:hydration/"):
                    native |= expand(tag, set())
        for item in sorted(native & all_ids):
            errors.append(f"TAN 原生補水標籤已涵蓋，請避免重複：{item}")
        print(f"TAN 原生標籤展開後 {len(native)} 個物品；與本模組重疊 {len(native & all_ids)} 個")
    for item in sorted(all_ids):
        if item.startswith("toughasnails:"):
            errors.append(f"TAN 原生物品不應重複設定：{item}")
    print(f"補水設定總計 {len(all_ids)} 個物品；錯誤 {len(errors)} 筆")
    for error in errors:
        print("錯誤：" + error)
    return int(bool(errors))

if __name__ == "__main__":
    raise SystemExit(main())
