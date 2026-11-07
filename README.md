# 飲食冷暖（Food Temperature Compatibility）

Minecraft 1.21.1 / NeoForge / Java 21

整合 Tough As Nails 的食物冷熱效果。食物溫度固定，不追蹤背包內物品的冷卻時間。

目前處於 alpha 開發階段，尚未通過 NeoForge 完整編譯及遊戲測試。GitHub Actions 將協助驗證建置。

## Alex's Caves Delight 1.0.28（0.1.15-alpha）

已以原始 JAR 的 `ModItems` 註冊字串和 `ModFoods` 食物屬性核對 81 種食物：40 種有固定升降溫、41 種維持中性；21 種液體或濕潤食物使用 Tough As Nails 原生補水標籤（湯品 7、飲品 6、少量補水 8）。毒醬製成的酸液飲品、純粹黑暗飲品不額外補水。TAN 標籤採 `required: false`，不用安裝此選用模組也不會缺物品。完整核對表見 `compatibility/alexscavesdelight_1.0.28_food_rules.json`。

除 GitHub Actions 編譯外，仍需實際遊戲測試不同食用動作與補水顯示。這是資料與程式層整合，不代表已進行遊戲驗證。

## 地城樂事 Dungeons Delight 1.5.2／甜點樂事 Sweet Delight 1.1.0（0.1.16-alpha）

本版新增兩種模組的固定食物冷熱及 Tough As Nails 原生補水標籤。依上傳 JAR 的物品模型／英文物品鍵核對，新增 70 筆需判定的項目（65 筆非零體溫、26 筆補水）；其中地城樂事 57 筆、甜點樂事 13 筆。一般蛋糕、餅乾、巧克力等甜點不因名稱含奶就自動補水；煉乳及淋醬也不當成一般可食用飲料。只在食用時處理，沒有背包冷卻計時。

已加入相應的進度 CSV、靜態審查台帳、TAN 標籤及相容性核對 JSON；仍須 GitHub Actions 建置以及進遊戲測試。物品模型／語言鍵存在不表示模組註冊或食用事件已在伺服器中驗證；詳細規則見 `compatibility/dungeonsdelight_sweet_delight_2026-11-08_food_rules.json`。
