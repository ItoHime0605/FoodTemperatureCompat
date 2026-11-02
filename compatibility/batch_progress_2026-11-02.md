# 飲食冷暖｜2026-11-02 大批次盤點與進度

## 計數基準（以此批 GitHub 設定及 CSV 為準）
- **目前已識別的食物／候選總數：909 項**。來自原有追蹤 555 項，以及 Extra Delight 官方 `1.21` 分支程式碼新增的 354 個不同 ID。
- **靜態第一輪分類：909／909（100%）**。每個 ID 都有「冷熱狀態、已設補水、含水特性初篩、下一步與驗證狀態」欄位，詳見 `full_food_static_audit_2026-11-02.csv`。這是**自動化名稱及既有設定初篩**，絕非全部已人工逐項核對配方，更不是遊戲實測完成。
- **已設定非零冷熱值：502／909（55.2%）**。其餘不一定要設值，可能為合理中性料理或尚未加入的候選。
- **已設定 TAN 補水：259／909（28.5%）**。其餘不一定應補水；偏乾食物應維持沒有額外補水。
- **來源碼食物相關註冊初篩：437／909（48.1%）**，全部來自 Extra Delight 官方 `1.21` 分支。437 指原始碼中使用 FoodProperties 或飲食物品建構方式的註冊項目；**不能代替使用者目前安裝版本的 JAR 驗證**。
- **各模組台帳「可食用性已核對數」合計：32／909（約 3.5%）**。這是台帳的來源碼／JAR 級保守核對數，包含 17 項 Extra Delight 詳審，不代表 32 項已通過遊戲實測。
- **有補水潛力但尚無本模組補水標籤：165 項（名稱／食材初篩候選）**。需要進一步用配方、食用屬性、原生 TAN 標籤判斷；不等於這 165 項全都需要補水。
- **實際安裝 JAR 與逐項遊戲內完成驗證：尚無可供統計的完整驗證紀錄**。不可把上面的靜態初篩 100% 說成開發已全部完成。

## 本輪已實際提交的功能變更
1. 以食材配方判斷，為 `extradelight:carrot_salad` 與 `extradelight:beet_mint_salad` 新增少量補水。
2. 再為七種先前尚未設定的 Extra Delight 食物新增補水：
   - `sliced_onion`、`grated_carrot`、`roasted_apple`、`potato_salad`：thirst 1／hydration 10。
   - `tomato_soup`、`borscht`、`sweet_berry_popsicle`：thirst 2／hydration 30。
3. `apple_popsicle` 原本已有 thirst 1／hydration 10，**本輪是改為 thirst 2／hydration 30，不是新增第八個補水物品**；已移除跨分類重複。
4. **補水總數從前一輪的 250 項提升到 259 項**（新增九項、調整一項）。原有冷熱設定 502 項不變；湯與冰品若官方來源有 TAN 原生加熱／冷卻標籤，此輪不另新增非零冷熱值。

## 待處理相容性風險
- Extra Delight 官方 `1.21` 分支現有 TAN `heating_consumed_items` 37 項、`cooling_consumed_items` 20 項；與本模組冷熱設定分別有 17 項與 14 項重疊，合計 **31 項可能重複作用**。見 `extradelight_native_tan_temperature_overlap_2026-11-02.md`。
- 官方 TAN thirst 來源另有 8 項與本模組自訂 thirst 重疊的已知紀錄，見 `extradelight_native_tan_overlap_2026-11-02.md`。
- 官方來源分支不等於使用者安裝的指定版本；對上述重疊先稽核、後依實際 JAR 和 TAN 解析行為確認，**不能貿然刪掉原本的補水或溫度功能**。

## 分母範圍與下階段工作
909 是**當下掌握的候選清單**，不是全部 23 個模組食物的最終數量；其餘模組完整註冊表若再發現可食用物品，分母將增長。
下一批以 `full_food_static_audit_2026-11-02.csv` 的 165 項含水候選優先，先驗證 ID、食物屬性、原生 TAN 標籤，再依份量分級；不得只靠單字聯想就直接改數值。

## 相關來源
- 本模組 GitHub： https://github.com/ItoHime0605/FoodTemperatureCompat
- Extra Delight `1.21` 官方來源： https://github.com/Lance5057/ExtraDelight/tree/1.21
