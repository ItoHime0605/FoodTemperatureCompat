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
        archive.writestr("assets/example/models/item/berry_juice.json", '{"parent":"item/generated"}')
        archive.writestr("assets/example/models/item/iron_sword.json", '{"parent":"item/handheld"}')
        archive.writestr("assets/example/models/item/tomato_salad.json", '{"parent":"item/generated"}')
    subprocess.run([sys.executable, str(ROOT / "tools/scan_food_candidates.py"), str(jar), "--output", str(output)], cwd=ROOT, check=True)
    with output.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert {row["候選物品 ID"] for row in rows} == {"example:berry_juice", "example:tomato_salad"}
    assert all(row["可食用性"] == "未確認" for row in rows)
    assert all(row["TAN 原生補水"] == "未確認" for row in rows)
print("候選掃描器測試通過")
