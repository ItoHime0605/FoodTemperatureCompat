#!/usr/bin/env python3
"""Alex's Caves Delight 1.0.28: audited registry IDs and runtime TAN data.

The expected SHA256 is computed from 81 ITEM registry names obtained from the
user-supplied 1.0.28 JAR's ModItems/ModFoods bytecode (sorted and newline joined).
This test does not pretend to run a Minecraft server.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path("src/main/resources")
DATA = ROOT / "data/toughasnails/tags/item"
RULES = Path("compatibility/alexscavesdelight_1.0.28_food_rules.json")
PREFIX = "alexscavesdelight:"
EXPECTED_REGISTRY_SHA256 = "1b5cce4f2a66186c9cf4bec26cae2587491e779da2274ca9d40a5a9b6e867a4b"
LEVELS = {
    "soup": ("thirst/2_thirst_drinks.json", "hydration/30_hydration_drinks.json", 2, 30),
    "drink": ("thirst/4_thirst_drinks.json", "hydration/50_hydration_drinks.json", 4, 50),
    "low_hydration": ("thirst/1_thirst_drinks.json", "hydration/10_hydration_drinks.json", 1, 10),
}


def csv_rows(name):
    with name.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def load_tag(relative):
    return [item["id"] if isinstance(item, dict) else item
            for item in json.loads((DATA / relative).read_text(encoding="utf-8"))["values"]]


def main():
    doc = json.loads(RULES.read_text(encoding="utf-8"))
    rules = doc["items"]
    ids = [item["id"] for item in rules]
    assert doc["jar_version"] == "1.0.28" and doc["count"] == 81
    assert len(ids) == len(set(ids)) == 81
    actual_hash = hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()
    assert actual_hash == EXPECTED_REGISTRY_SHA256, "JAR 註冊 ID 有缺漏或拼錯"
    assert len([x for x in rules if x["temperature"]]) == 40
    assert len([x for x in rules if not x["temperature"]]) == 41
    assert len([x for x in rules if x["hydration_group"]]) == 21
    assert not any("knife" in item for item in ids)

    # Runtime thermal table and full progress list must match this reviewed manifest.
    temps = {}
    for line in (ROOT / "food_temperature_tiers.txt").read_text(encoding="utf-8").splitlines():
        stripped = line.split("#", 1)[0].strip()
        if stripped and stripped.startswith(PREFIX):
            key, value = stripped.split("=", 1)
            assert key not in temps
            temps[key] = float(value)
    expected_temps = {x["id"]: float(x["temperature"]) for x in rules if x["temperature"]}
    assert temps == expected_temps, "溫度表與核對清單不一致"

    progress = [x for x in csv_rows(Path("compatibility/food_item_progress.csv"))
                if x["物品 ID"].startswith(PREFIX)]
    assert len(progress) == 81
    assert {x["物品 ID"]: float(x["設定溫度值"]) for x in progress} == {
        x["id"]: float(x["temperature"]) for x in rules}
    for item in progress:
        if float(item["設定溫度值"]) == 0:
            assert "中性" in item["分類狀態"]

    neutral = {x["物品 ID"]: x for x in csv_rows(Path("compatibility/neutral_hydration_review.csv"))
               if x["物品 ID"].startswith(PREFIX)}
    assert set(neutral) == {x["id"] for x in rules if not x["temperature"]}
    for item in rules:
        if item["id"] in neutral:
            target = "已設定少量補水" if item["hydration_group"] == "low_hydration" else "暫不補水"
            assert neutral[item["id"]]["補水判定"] == target

    # Every hydrated item must have ONE thirst tier, ONE hydration tier, and the TAN drinks entry.
    tagged = {}
    for relative in [
        "thirst/1_thirst_drinks.json", "thirst/2_thirst_drinks.json",
        "thirst/3_thirst_drinks.json", "thirst/4_thirst_drinks.json",
        "thirst/6_thirst_drinks.json", "hydration/10_hydration_drinks.json",
        "hydration/20_hydration_drinks.json", "hydration/30_hydration_drinks.json",
        "hydration/50_hydration_drinks.json", "drinks.json",
    ]:
        members = load_tag(relative)
        assert len(members) == len(set(members)), "標籤有重複 ID：" + relative
        tagged[relative] = {x for x in members if x.startswith(PREFIX)}
    for item in rules:
        tag_group = item["hydration_group"]
        expect = (LEVELS[tag_group][:2] + ("drinks.json",)) if tag_group else ()
        matched = tuple(path for path in tagged if item["id"] in tagged[path])
        assert set(matched) == set(expect), f"補水標籤不一致：{item['id']} {matched} != {expect}"

    audits = {x["物品 ID"]: x for x in csv_rows(Path("compatibility/full_food_static_audit_2026-11-02.csv"))
              if x["物品 ID"].startswith(PREFIX)}
    assert len(audits) == 81
    for item in rules:
        row = audits[item["id"]]
        group = item["hydration_group"]
        th, hy = LEVELS[group][2:] if group else ("", "")
        assert row["已有冷熱設定值"] == (str(item["temperature"]) if item["temperature"] else "")
        assert row["TAN 口渴標籤階級"] == str(th)
        assert row["TAN 補水標籤階級"] == str(hy)

    ledger = [x for x in csv_rows(Path("compatibility/compat_mod_review_status.csv"))
              if x["modid"] == "alexscavesdelight"]
    assert len(ledger) == 1
    for field, value in [("冷熱設定筆數", 40), ("補水設定筆數", 21),
                         ("已列入審查表筆數", 41), ("可食用性已核對數（保守估計）", 81)]:
        assert int(ledger[0][field]) == value

    print("Alex's Caves Delight 1.0.28：81 種食物；冷熱 40 筆；中性 41 筆；補水 21 筆")
    print("原 JAR 81 個註冊 ID 指紋一致；TAN 標籤／進度／稽核／台帳一致，靜態測試通過")


if __name__ == "__main__":
    main()
