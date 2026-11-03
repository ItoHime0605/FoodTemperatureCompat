package tw.zonezero.foodtemp;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.ChatFormatting;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;

/** 在物品提示中顯示固定冷熱方向，不將小數值誤稱為 TAN 體溫階級。 */
public final class FoodTemperatureTooltip {
    private final FoodTierRegistry registry;

    public FoodTemperatureTooltip(FoodTierRegistry registry) {
        this.registry = registry;
    }

    @SubscribeEvent
    public void onTooltip(ItemTooltipEvent event) {
        if (event.getItemStack().isEmpty()) return;
        String id = BuiltInRegistries.ITEM.getKey(event.getItemStack().getItem()).toString();
        // Tough As Nails 自帶提示；不重複標示其原生物品。
        if (id.startsWith("toughasnails:")) return;
        // Avoid displaying our custom effect on foods handled natively by TAN.
        if (TanNativeConsumptionGuard.hasNativeTemperature(event.getItemStack())) return;
        double tier = registry.tier(id);
        if (tier == 0.0) return;
        String value = java.math.BigDecimal.valueOf(Math.abs(tier)).stripTrailingZeros().toPlainString();
        boolean warming = tier > 0;
        MutableComponent label = Component.translatable(warming ? "tooltip.foodtemperaturecompat.warming" : "tooltip.foodtemperaturecompat.cooling")
                .withStyle(warming ? ChatFormatting.GOLD : ChatFormatting.AQUA);
        event.getToolTip().add(Component.literal("❖ ").withStyle(ChatFormatting.GRAY)
                .append(label)
                .append(Component.translatable("tooltip.foodtemperaturecompat.value", (warming ? "+" : "-") + value)
                        .withStyle(ChatFormatting.GRAY)));
    }
}
