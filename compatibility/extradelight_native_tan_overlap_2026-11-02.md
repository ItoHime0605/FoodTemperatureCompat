# Extra Delight 原生 TAN 重疊稽核（2026-11-02）

來源：官方 GitHub 1.21 分支（非指定版本 JAR）
- https://github.com/Lance5057/ExtraDelight/blob/1.21/src/generated/resources/data/toughasnails/tags/item/thirst/2_thirst_drinks.json
- https://github.com/Lance5057/ExtraDelight/blob/1.21/src/generated/resources/data/toughasnails/tags/item/thirst/4_thirst_drinks.json
- https://github.com/Lance5057/ExtraDelight/blob/1.21/src/generated/resources/data/toughasnails/tags/item/thirst/6_thirst_drinks.json
- https://github.com/Lance5057/ExtraDelight/blob/1.21/src/main/java/com/lance5057/extradelight/ExtraDelightItems.java

## 與本模組 thirst 標籤重疊的 8 項
| 物品 ID | Extra Delight 官方 thirst 階級 | 本模組 thirst 階級 |
|---|---:|---:|
| extradelight:coffee | 2 | 4 |
| extradelight:dalgona_coffee | 4 | 4 |
| extradelight:apple_milkshake | 2 | 4 |
| extradelight:cactus_juice | 6 | 4 |
| extradelight:chocolate_milkshake | 2 | 4 |
| extradelight:glow_berry_juice | 6 | 4 |
| extradelight:glow_berry_milkshake | 2 | 4 |
| extradelight:milkshake | 2 | 4 |

## 審查結論
- 官方來源明確包含 thirst 2、4、5、6、8 階級的資料標籤；本模組現有驗證器只讀取自身 1～4 階級，不足以判定所有跨模組重疊。
- 本模組現有 hydration 標籤是另一套資料，不應未核對 TAN 實際解析規則就直接刪除。
- 以上為**官方來源分支**核對，尚未核對使用者實際安裝的 Extra Delight JAR 版本；因此暫不修改正式 thirst/hydration 數值，避免造成補水功能退化。
- 先前候選清單把部分已設置補水的 Extra Delight 飲品誤列為「未加入補水」，已在審查表更正。
