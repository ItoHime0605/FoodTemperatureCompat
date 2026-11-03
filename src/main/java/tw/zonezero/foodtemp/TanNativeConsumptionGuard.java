package tw.zonezero.foodtemp;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

/**
 * Respects native Tough As Nails consumable-temperature data packs.
 * Custom food temperature is not stacked on an already supported TAN consumable.
 */
public final class TanNativeConsumptionGuard {
    private static final TagKey<Item> NATIVE_COOLING = TagKey.create(
            Registries.ITEM, ResourceLocation.fromNamespaceAndPath("toughasnails", "cooling_consumed_items"));
    private static final TagKey<Item> NATIVE_HEATING = TagKey.create(
            Registries.ITEM, ResourceLocation.fromNamespaceAndPath("toughasnails", "heating_consumed_items"));

    private TanNativeConsumptionGuard() {}

    public static boolean hasNativeTemperature(ItemStack item) {
        return !item.isEmpty() && (item.is(NATIVE_COOLING) || item.is(NATIVE_HEATING));
    }
}
