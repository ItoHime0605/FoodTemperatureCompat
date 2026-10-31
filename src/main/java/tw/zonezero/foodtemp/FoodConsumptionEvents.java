package tw.zonezero.foodtemp;
import net.minecraft.core.registries.BuiltInRegistries;
import java.util.Map;
import java.util.TreeMap;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.entity.living.LivingEntityUseItemEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
public final class FoodConsumptionEvents {
    private static final Logger LOGGER = LoggerFactory.getLogger("foodtemperaturecompat");
    private final ConsumptionBridge bridge;
    private final FoodTierRegistry registry;
    public FoodConsumptionEvents(ConsumptionBridge bridge, FoodTierRegistry registry) {
        this.bridge = bridge;
        this.registry = registry;
    }
    @SubscribeEvent
    public void onServerStarted(ServerStartedEvent event) {
        int missing = 0;
        Map<String, int[]> byMod = new TreeMap<>();
        for (String id : registry.entries().keySet()) {
            ResourceLocation key = ResourceLocation.parse(id);
            int[] stats = byMod.computeIfAbsent(key.getNamespace(), unused -> new int[2]);
            stats[0]++;
            if (!BuiltInRegistries.ITEM.containsKey(key) || BuiltInRegistries.ITEM.get(key) == Items.AIR) {
                missing++;
                stats[1]++;
                LOGGER.warn("[飲食冷暖] 找不到設定中的物品 ID：{}；此項冷熱效果不會觸發。", id);
            }
        }
        for (Map.Entry<String, int[]> entry : byMod.entrySet()) {
            LOGGER.info("[飲食冷暖] 模組 {}：設定 {} 筆，未註冊 {} 筆。",
                    entry.getKey(), entry.getValue()[0], entry.getValue()[1]);
        }
        LOGGER.info("[飲食冷暖] 已載入 {} 筆食物溫度設定，{} 筆物品 ID 未註冊。", registry.size(), missing);
    }
    @SubscribeEvent
    public void onFinishedUsing(LivingEntityUseItemEvent.Finish event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) return;
        String id = BuiltInRegistries.ITEM.getKey(event.getItem().getItem()).toString();
        if (!bridge.isConfigured(id)) return;
        bridge.consumed(player.getUUID(), id, player.getServer().getTickCount());
    }
    @SubscribeEvent
    public void onServerStopped(ServerStoppedEvent event) { bridge.clear(); }
    @SubscribeEvent
    public void onLogout(PlayerEvent.PlayerLoggedOutEvent event) {
        bridge.logout(event.getEntity().getUUID());
    }
}