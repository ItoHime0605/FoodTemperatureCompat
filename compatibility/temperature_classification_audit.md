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

## 第三批模型資源交叉驗證（2026-11-01）
已直接使用本次工作環境中上傳的 NeoForge JAR，檢查各 `assets/<namespace>/models/item/<item>.json` 的實際存在性，而非僅依據物品名稱推測：

| 命名空間 | 已檢查第三批候選 | 找不到模型 |
|---|---:|---:|
| kaleidoscope_cookery | 15 | 0 |
| alexsmobsdelight | 42 | 0 |
| delightful | 13 | 0 |
| starcatcher_delight | 3 | 0 |
| festive_delight | 1 | 0 |
| **總計** | **74** | **0** |

注意：同一資源命名空間也可能出現在相容性補丁 JAR 中；此次已確認 `kaleidoscope_cookery` 的 15 個候選模型也存在於廚房主模組 JAR。

此外，`kaleidoscope_tavern` 的 `watermelon_juice`、`mojito` 已從酒館 JAR 模型清單確認並加入候選冷飲。酒精效果與原模組的飲用機制仍需測試，不能僅以模型存在認定生效。

## 靜態設定格式稽核
已直接核對 GitHub 上本輪修改前的 217 筆設定：**重複 ID 0 筆、格式錯誤 0 筆、階級超界 0 筆**。後續新增酒館 2 筆，完整整合測試時需重新執行稽核工具。

