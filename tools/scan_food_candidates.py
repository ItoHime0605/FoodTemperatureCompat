#!/usr/bin/env python3
"""從模組 JAR 盤點可能含水的物品；僅列候選，不推定可食用或直接設定補水。"""
import argparse
import csv
import json
import re
import zipfile
from pathlib import Path

CATEGORIES = {
    "水果": ("fruit", "berry", "melon", "apple", "pear", "peach", "grape", "lychee", "mango", "orange", "kiwi", "pineapple", "lemon", "lime"),
    "蔬菜": ("vegetable", "tomato", "cucumber", "lettuce", "cabbage", "carrot", "beetroot", "radish", "pepper"),
    "沙拉": ("salad",),
    "飲品": ("juice", "drink", "tea", "coffee", "milkshake", "smoothie", "water", "lemonade"),
    "湯品": ("soup", "broth", "stew", "porridge", "congee"),
    "冰品": ("ice_cream", "popsicle", "sorbet", "gelato"),
    "高含水料理": ("jelly", "pudding", "custard", "yogurt", "yoghurt", "tofu", "coconut", "watermelon", "gazpacho"),
}
# 模型名稱中的食物關鍵字不代表該物品可以食用；先排除明顯的容器與裝飾模型。
NONFOOD_SUFFIXES = ("_bucket", "_bottle_empty", "_bottle_block", "_crate", "_block", "_seeds", "_seed", "_sapling", "_leaves", "_log", "_planks", "_door", "_trapdoor", "_sign", "_hanging_sign", "_candle", "_wall", "_stairs", "_slab", "_fence", "_fence_gate", "_spawn_egg", "_knife", "_sword", "_axe", "_pickaxe", "_shovel", "_hoe")
NONFOOD_PREFIXES = ("empty_", "raw_material_")
MODEL = re.compile(r"^assets/([a-z0-9_.-]+)/models/item/([a-z0-9_./-]+)\.json$")
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jars", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, default=Path("compatibility/food_candidates_from_jars.csv"))
    args = parser.parse_args()
    known = set()
    for source in (Path("compatibility/neutral_hydration_review.csv"), Path("compatibility/food_item_progress.csv")):
        if source.exists():
            with source.open(encoding="utf-8-sig", newline="") as f:
                known.update(row["物品 ID"].strip() for row in csv.DictReader(f))
    rows = []
    seen = set()
    for jar_path in args.jars:
        with zipfile.ZipFile(jar_path) as jar:
            for name in sorted(jar.namelist()):
                match = MODEL.fullmatch(name)
                if not match:
                    continue
                namespace, item = match.groups()
                # 僅辨識頂層物品模型；子目錄可能是材質變體、GUI 或非註冊物品。
                if "/" in item or item.endswith(NONFOOD_SUFFIXES) or item.startswith(NONFOOD_PREFIXES):
                    continue
                category = next((cat for cat, words in CATEGORIES.items() if any(word in item for word in words)), None)
                if not category:
                    continue
                try:
                    json.loads(jar.read(name))
                except (ValueError, UnicodeDecodeError):
                    continue
                identifier = f"{namespace}:{item}"
                # 不將同一 JAR 中重複的模型路徑計算成不同物品。
                if (jar_path.name, identifier) in seen:
                    continue
                seen.add((jar_path.name, identifier))
                rows.append({
                    "來源 JAR": jar_path.name, "候選物品 ID": identifier, "可能分類": category,
                    "既有進度紀錄": "已有" if identifier in known else "未收錄",
                    "可食用性": "未確認", "TAN 原生補水": "未確認",
                    "建議": "僅供審查，禁止自動加入補水標籤",
                })
    rows.sort(key=lambda row: (row["來源 JAR"], row["候選物品 ID"]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["來源 JAR", "候選物品 ID", "可能分類", "既有進度紀錄", "可食用性", "TAN 原生補水", "建議"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"掃描 {len(args.jars)} 個 JAR，列出 {len(rows)} 個候選；輸出：{args.output}")

if __name__ == "__main__":
    main()
