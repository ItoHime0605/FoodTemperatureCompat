# 飲食冷暖｜第二批食物冷熱分類審核（尚未編譯）

## 本輪實際變更
- 已把 **91 個**不同的 `namespace:item_id` 加入 `src/main/resources/food_temperature_tiers.txt`，涉及 Extra Delight、Fruits Delight、Veggies Delight、Collector's Reap、Pineapple Delight、Corn Delight 六款模組。
- 原始參考為使用者上傳之對應 NeoForge 1.21.1 JAR 的 `assets/*/models/item/*.json` 路徑。此證據僅確認模型資源存在，**不能直接證明物品已註冊、可食用、溫度、實際使用事件或翻譯名稱**。
- 冷熱階級為暫定設計：湯／燉菜／熱咖啡 +2；冰淇淋／冰棒 -2；果汁／奶昔／部分茶飲 -1。這是分類策略，不是作者官方溫度數據。
- **未加入**流體桶、料理方塊、茶包、咖啡豆、作物及材料；仍需後續驗證。

## 待完成驗證
1. 啟動後檢查物品註冊表，處理啟動日誌中的缺失 ID。
2. 確認各物品是可食用物品，且 `LivingEntityUseItemEvent.Finish` 在實際飲食時觸發。
3. 檢查帶有特殊飲用行為的酒精、茶飲與其他飲品，不要重複套用模組原有的體溫或酒精效果。
4. 驗證 Tough As Nails 的溫度偏移、累積上限、時間衰退與玩家離線清除。
5. 全階段完成後，才手動執行 GitHub Actions 編譯；目前工作流程已改為 `workflow_dispatch`。

## 性能原則
僅在食用完成及 TAN 查詢溫度時處理資料；不逐 tick 掃描背包，不追蹤食物在背包中的冷卻或加熱。
