# 飲食冷暖｜Extra Delight 與 TAN 原生冷熱標籤重疊查核
查核日期：2026-11-02
來源：Extra Delight 官方 1.21 分支原始碼所生成的 TAN 標籤；**不等於使用者實際安裝 JAR 的已核對內容**。
來源：
- https://github.com/Lance5057/ExtraDelight/blob/1.21/src/generated/resources/data/toughasnails/tags/item/heating_consumed_items.json
- https://github.com/Lance5057/ExtraDelight/blob/1.21/src/generated/resources/data/toughasnails/tags/item/cooling_consumed_items.json
- 本專案：`src/main/resources/food_temperature_tiers.txt`

## 比對數量
- 官方加熱標籤：37 項；與本模組冷熱設定重疊 **17 項**。
- 官方冷卻標籤：20 項；與本模組冷熱設定重疊 **14 項**。
- 合計 **31 項可能重複施加冷熱效果**。這是設定層級重疊證據，不等於已證明遊戲內加成兩次。
- 此外官方另有 27 項 TAN thirst 飲品標籤；其與本模組的重疊另記於 `compatibility/extradelight_native_tan_overlap_2026-11-02.md`。

## 重疊：TAN 原生加熱
| 物品 ID | 本模組溫度值 |
|---|---:|
| `extradelight:gourmet_hot_chocolate` | +2 |
| `extradelight:coffee` | +2 |
| `extradelight:dalgona_coffee` | +2 |
| `extradelight:potato_soup` | +2 |
| `extradelight:fish_soup` | +2 |
| `extradelight:carrot_soup` | +2 |
| `extradelight:pork_stew` | +2 |
| `extradelight:lamb_stew` | +2 |
| `extradelight:chicken_stew` | +2 |
| `extradelight:curry` | +0.6 |
| `extradelight:curry_rice` | +0.5 |
| `extradelight:oxtail_soup` | +2 |
| `extradelight:cactus_soup` | +2 |
| `extradelight:mulligatawny_soup` | +2 |
| `extradelight:jalapeno_stuffed_potato` | +0.5 |
| `extradelight:hazelnut_soup` | +2 |
| `extradelight:onion_soup` | +2 |

## 重疊：TAN 原生降溫
| 物品 ID | 本模組溫度值 |
|---|---:|
| `extradelight:glow_berry_popsicle` | -2 |
| `extradelight:fudge_popsicle` | -2 |
| `extradelight:honey_popsicle` | -2 |
| `extradelight:apple_popsicle` | -2 |
| `extradelight:caramel_popsicle` | -2 |
| `extradelight:ice_cream` | -2 |
| `extradelight:chocolate_ice_cream` | -2 |
| `extradelight:glow_berry_ice_cream` | -2 |
| `extradelight:pumpkin_ice_cream` | -2 |
| `extradelight:honey_ice_cream` | -2 |
| `extradelight:apple_ice_cream` | -2 |
| `extradelight:cookie_dough_ice_cream` | -2 |
| `extradelight:mint_chip_ice_cream` | -2 |
| `extradelight:grapefruit_sorbet` | -2 |

## 處理原則
1. 先取得使用者**實際安裝版本**的 Extra Delight JAR 及 TAN 10.1.0.13 標籤，核對上述標籤在實際版本是否存在。
2. 再確認 TAN 原生飲食冷熱事件與本模組 `LivingEntityUseItemEvent.Finish` 的累加時機，避免重複計算；冷熱效果可能疊加，先不武斷斷言已疊加。
3. **本次沒有直接刪除原有冷熱設定**，避免原版本沒有原生標籤時失去預期效果。
4. 對新發現的 `tomato_soup`、`borscht` 等含水湯品僅新增 TAN 補水，不額外新增冷熱數值；官方來源已帶原生加熱標籤。
