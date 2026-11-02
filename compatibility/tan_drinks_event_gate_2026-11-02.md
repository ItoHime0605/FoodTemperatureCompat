# TAN 10.1.0.13：口渴事件的必要標籤及 Extra Delight 重疊風險

查核：2026-11-02。此為 Minecraft 1.21.1 相容性**來源碼分析**；仍待使用者實際伺服器與相同 JAR 版本驗證。

## 已確認的 TAN 原始碼機制
官方 Tough As Nails `1.21.1` 分支：
- [ThirstHandler.java](https://github.com/Glitchfiend/ToughAsNails/blob/1.21.1/common/src/main/java/toughasnails/thirst/ThirstHandler.java) 的 `onItemUseFinish` 僅在 `drink.is(ModTags.Items.DRINKS)` 時讀取口渴值、補水值並呼叫 `thirst.drink(...)`。
- [ModTags.java](https://github.com/Glitchfiend/ToughAsNails/blob/1.21.1/common/src/main/java/toughasnails/init/ModTags.java) 的 `getThirstRestored` 按 1 → 20 順序查 `thirst/<階級>_thirst_drinks`；**多個口渴階級重疊時會取最小命中的階級**。
- `ThirstHandler` 的 hydration 讀取獨立於 thirst 階級；可依 `hydration/10_hydration_drinks` 等標籤額外指定 0.1、0.2、0.3、0.5 等補水值。但物品仍必須先在 `toughasnails:drinks`。
- 因此只在 thirst、hydration 標籤加入水果、沙拉、料理，而未讓它們加入 `drinks`，**在上述來源碼版本的預設飲食完成事件裡不會觸發補水**。

## 本輪實際修正
已新增：
`src/main/resources/data/toughasnails/tags/item/drinks.json`
- `replace:false`；保留 TAN 及其他模組既有的 drinks 標籤。
- 將本模組 283 個已有配對 thirst/hydration 標籤的 ID 全部納入。
- 每個條目均 `required:false`，缺少選用模組時不造成資料包載入失敗。
- 同步在 `tools/check_thirst_tags.py` 驗證：任何新增補水食物若漏掉 drinks 標籤，CI 直接失敗。
- 此修正沒有改動 502 項冷熱數值，也不會讓一般不可食用道具自動變成可食用；仍依原模組食用事件觸發。

## Extra Delight 特別注意
官方 [Extra Delight 1.21 EDItemTags.java](https://github.com/Lance5057/ExtraDelight/blob/1.21/src/main/java/com/lance5057/extradelight/data/EDItemTags.java) `parseTaNTag` 的 hydration switch 使用 1～10 對應 10～100 的標籤，但 [ExtraDelightItems.java](https://github.com/Lance5057/ExtraDelight/blob/1.21/src/main/java/com/lance5057/extradelight/ExtraDelightItems.java) 許多飲品 `setHydration(20)`、`setHydration(30)` 等。官方分支的生成資源樹中未找到對應 hydration tags。

這表示該分支存在**疑似原生補水標籤無法生成的條件不一致**；不是已確認使用者安裝的 JAR 也有此問題。
- 官方 TAN thirst 在 `extradelight:cactus_juice`／`glow_berry_juice` 是 6，但本模組既有 thirst 設定是 4，按 TAN 逐級匹配的規則可能導致原生 thirst 6 被 4 優先覆蓋。
- 同步存在多筆 Extra Delight 原生 TAN 冷熱標籤與本模組自訂效果重疊（參見 `extradelight_native_tan_temperature_overlap_2026-11-02.md`）。
- **本次未修改這些尚未依實際安裝版本核實的原生階級**，避免版本不相同時破壞已存在效果。

## 待實機驗證
1. TAN 10.1.0.13 與實際 Extra Delight JAR 的組合是否確實吃到上述標籤。
2. 飲用水、果汁、水果與沙拉的食用完成事件是否恢復設定的 thirst 與 hydration。
3. 某些自訂 `finishUsingItem`、特殊容量飲品，是否有模組自身直接呼叫 `thirst.drink` 導致重複。
4. 官方原生加熱／冷卻標籤與本模組冷熱累加器是否疊加。
