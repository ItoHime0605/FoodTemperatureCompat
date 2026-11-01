#!/usr/bin/env python3
"""使用臨時 JAR 驗證候選掃描器，不需要下載第三方模組。"""
import csv
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    folder = Path(tmp)
    jar = folder / "sample.jar"
    output = folder / "candidates.csv"
    with zipfile.ZipFile(jar, "w") as archive:
        archive.writestr("assets/example/items/berry_juice.json", '{"model":{"type":"minecraft:model","model":"example:item/berry_juice"}}')
        archive.writestr("assets/example/items/pear_juice.json", '{"model":{"type":"minecraft:model","model":"example:item/pear_juice"}}')
        archive.writestr("assets/example/items/broken_juice.json", "{bad json")
        archive.writestr("assets/example/models/item/broken_juice.json", '{"parent":"item/generated"}')
        archive.writestr("assets/example/items/broken_model_juice.json", '{"model":{"type":"minecraft:model","model":"example:item/broken_model_juice"}}')
        archive.writestr("assets/example/models/item/broken_model_juice.json", "{bad json")
        archive.writestr("assets/example/items/array_juice.json", "[]")
        archive.writestr("assets/example/models/item/array_juice.json", '{"parent":"item/generated"}')
        archive.writestr("assets/example/models/item/null_juice.json", "null")
        archive.writestr("assets/example/models/item/berry_juice.json", '{"parent":"item/generated"}')
        archive.writestr("assets/example/models/item/iron_sword.json", '{"parent":"item/handheld"}')
        archive.writestr("assets/example/models/item/tomato_salad.json", '{"parent":"item/generated"}')
        archive.writestr("assets/example/models/item/coconut_pudding.json", '{"parent":"item/generated"}')
        archive.writestr("assets/example/models/item/invalid_juice.json", "{bad json")
        archive.writestr("assets/example/models/item/water_bucket.json", '{"parent":"item/generated"}')
        archive.writestr("assets/example/models/item/tomato_seeds.json", '{"parent":"item/generated"}')
        archive.writestr("assets/example/models/item/fruit_crate.json", '{"parent":"item/generated"}')
        archive.writestr("assets/example/models/item/variants/berry_juice.json", '{"parent":"item/generated"}')
    subprocess.run([sys.executable, str(ROOT / "tools/scan_food_candidates.py"), str(jar), "--output", str(output)], cwd=ROOT, check=True)
    with output.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert {row["候選物品 ID"] for row in rows} == {"example:berry_juice", "example:pear_juice", "example:tomato_salad", "example:coconut_pudding"}
    assert next(row["可能分類"] for row in rows if row["候選物品 ID"] == "example:coconut_pudding") == "高含水料理"
    assert next(row for row in rows if row["候選物品 ID"] == "example:berry_juice")["物品定義檔"] == "存在"
    assert next(row for row in rows if row["候選物品 ID"] == "example:pear_juice")["物品模型"] == "未找到"
    assert all(row["可食用性"] == "未確認" for row in rows)
    assert all(row["TAN 原生補水"] == "未確認" for row in rows)
    # 不同資料夾中的同名 JAR 不可因檔名相同而漏掉候選。
    first_dir = folder / "first"
    second_dir = folder / "second"
    first_dir.mkdir()
    second_dir.mkdir()
    first_jar = first_dir / "same.jar"
    second_jar = second_dir / "same.jar"
    for target in (first_jar, second_jar):
        with zipfile.ZipFile(target, "w") as archive:
            archive.writestr("assets/example/items/pear_juice.json", '{"model":{"type":"minecraft:model","model":"example:item/pear_juice"}}')
    subprocess.run([sys.executable, str(ROOT / "tools/scan_food_candidates.py"), str(first_jar), str(second_jar), "--output", str(output)], cwd=ROOT, check=True)
    with output.open(encoding="utf-8-sig", newline="") as handle:
        duplicate_name_rows = list(csv.DictReader(handle))
    assert len(duplicate_name_rows) == 2
    assert all(row["候選物品 ID"] == "example:pear_juice" for row in duplicate_name_rows)
print("候選掃描器測試通過")
