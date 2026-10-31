#!/usr/bin/env python3
"""對照最初的候選 CSV 與目前冷熱設定；只輸出差集，不重複列為新工作。"""
import argparse
import csv
from collections import Counter
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("review_csv", type=Path, help="初期 item_tiers_review.csv")
    parser.add_argument("--tiers", type=Path, default=Path("src/main/resources/food_temperature_tiers.txt"))
    parser.add_argument("--output", type=Path, default=Path("compatibility/review_remaining.csv"))
    args = parser.parse_args()
    configured = {}
    for line in args.tiers.read_text(encoding="utf-8").splitlines():
        value = line.split("#", 1)[0].strip()
        if not value:
            continue
        item_id, tier = value.split("=", 1)
        configured[item_id.strip()] = int(tier.strip())
    with args.review_csv.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    ids = [row["物品 ID"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("候選 CSV 含重複物品 ID，請先去重")
    remaining = [row for row in rows if row["物品 ID"] not in configured]
    already = [row for row in rows if row["物品 ID"] in configured]
    review_required = [row for row in remaining if row["建議溫度階級"].strip() != "0"]
    neutral = [row for row in remaining if row["建議溫度階級"].strip() == "0"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[*rows[0].keys(), "處理狀態"] if rows else ["物品 ID", "處理狀態"])
        writer.writeheader()
        for row in remaining:
            writer.writerow({**row, "處理狀態": "待人工判定" if row["建議溫度階級"].strip() != "0" else "未分類／預設中性"})
    print(f"原始候選：{len(rows)}")
    print(f"候選中已設定：{len(already)}")
    print(f"候選中尚未設定：{len(remaining)}")
    print(f"尚未設定且建議非中性（優先審核）：{len(review_required)}")
    print(f"尚未設定且建議中性（不應自動當成待做）：{len(neutral)}")
    print(f"設定檔中不在候選 CSV 的項目：{len(set(configured) - set(ids))}")
    print(f"輸出：{args.output}")
    print("注意：已設定≠已完成物品註冊／可食用性／體溫效果驗證。")
if __name__ == "__main__":
    main()
