#!/usr/bin/env python3
"""確認冷熱設定與進度 CSV 完全一致；不需要啟動 Minecraft 或編譯。"""
import argparse
import csv
import math
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tiers", type=Path, default=Path("src/main/resources/food_temperature_tiers.txt"))
    parser.add_argument("--progress", type=Path, default=Path("compatibility/food_item_progress.csv"))
    args = parser.parse_args()
    tiers = {}
    errors = []
    for line_no, raw in enumerate(args.tiers.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        try:
            item_id, value = line.split("=", 1)
            item_id = item_id.strip()
            tier = float(value.strip())
        except ValueError:
            errors.append(f"設定第 {line_no} 行格式錯誤")
            continue
        if not math.isfinite(tier) or not -3 <= tier <= 3:
            errors.append(f"設定第 {line_no} 行溫度超出範圍")
        if tier == 0.0:
            errors.append(f"設定第 {line_no} 行為中性料理，應只記錄於進度表：{item_id}")
        if item_id in tiers:
            errors.append(f"設定重複 ID：{item_id}")
        tiers[item_id] = tier
    progress = {}
    neutral = set()
    with args.progress.open(encoding="utf-8-sig", newline="") as handle:
        for row_no, row in enumerate(csv.DictReader(handle), 2):
            item_id = row["物品 ID"].strip()
            if item_id in progress:
                errors.append(f"進度表重複 ID：{item_id}（第 {row_no} 行）")
            try:
                value = float(row["設定溫度值"])
                if not math.isfinite(value) or not -3 <= value <= 3:
                    raise ValueError("out of range")
                progress[item_id] = value
                if value == 0.0 and "中性" in row.get("分類狀態", ""):
                    neutral.add(item_id)
            except (TypeError, ValueError):
                errors.append(f"進度表第 {row_no} 行溫度無效")
    for item_id in sorted(tiers.keys() - progress.keys()):
        errors.append(f"進度表缺少：{item_id}")
    for item_id in sorted(progress.keys() - tiers.keys()):
        # 中性食物保留在追蹤表，但不必寫入執行時的非零溫度設定。
        # 非零值若遺漏設定仍視為錯誤。
        if item_id not in neutral:
            errors.append(f"進度表多出未明確標記中性的設定：{item_id}")
    for item_id in sorted(tiers.keys() & progress.keys()):
        if tiers[item_id] != progress[item_id]:
            errors.append(f"數值不一致：{item_id}（設定 {tiers[item_id]}／進度 {progress[item_id]}）")
    print(f"設定 {len(tiers)} 筆；進度 {len(progress)} 筆；錯誤 {len(errors)} 筆")
    for error in errors:
        print("錯誤：" + error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
