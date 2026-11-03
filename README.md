# 飲食冷暖（Food Temperature Compatibility）

Minecraft 1.21.1 / NeoForge / Java 21

整合 Tough As Nails 的食物冷熱效果。食物溫度固定，不追蹤背包內物品的冷卻時間。

目前處於 alpha 開發階段，尚未通過 NeoForge 完整編譯及遊戲測試。GitHub Actions 將協助驗證建置。

## Alex's Caves Delight 1.0.28（0.1.15-alpha）

已以原始 JAR 的 `ModItems` 註冊字串和 `ModFoods` 食物屬性核對 81 種食物：40 種有固定升降溫、41 種維持中性；21 種液體或濕潤食物使用 Tough As Nails 原生補水標籤（湯品 7、飲品 6、少量補水 8）。毒醬製成的酸液飲品、純粹黑暗飲品不額外補水。TAN 標籤採 `required: false`，不用安裝此選用模組也不會缺物品。完整核對表見 `compatibility/alexscavesdelight_1.0.28_food_rules.json`。

除 GitHub Actions 編譯外，仍需實際遊戲測試不同食用動作與補水顯示。這是資料與程式層整合，不代表已進行遊戲驗證。
