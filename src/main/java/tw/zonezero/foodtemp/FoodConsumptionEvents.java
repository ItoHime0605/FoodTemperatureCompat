package tw.zonezero.foodtemp;
import net.minecraft.core.registries.BuiltInRegistries;
import java.util.Map;
import java.util.TreeMap;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.UseAnim;
import net.minecraft.core.component.DataComponents;
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
        int needsConsumptionVerification = 0;
        Map<String, int[]> byMod = new TreeMap<>();
        for (String id : registry.entries().keySet()) {
            ResourceLocation key = ResourceLocation.parse(id);
            int[] stats = byMod.computeIfAbsent(key.getNamespace(), unused -> new int[2]);
            stats[0]++;
            if (!BuiltInRegistries.ITEM.containsKey(key) || BuiltInRegistries.ITEM.get(key) == Items.AIR) {
                missing++;
                stats[1]++;
                LOGGER.warn("[飲食冷暖] 找不到設定中的物品 ID：{}；此項冷熱效果不會觸發。", id);
            } else {
                // Default stacks provide only a preliminary check. Custom items may
                // add food components or consumption animations dynamically.
                var stack = BuiltInRegistries.ITEM.get(key).getDefaultInstance();
                UseAnim animation = stack.getUseAnimation();
                if (!stack.has(DataComponents.FOOD)
                        && animation != UseAnim.EAT && animation != UseAnim.DRINK) {
                    needsConsumptionVerification++;
                    LOGGER.warn("[飲食冷暖] 物品 {} 預設狀態沒有 FOOD 或飲食動畫；需確認其自訂食用流程，不能直接認定可食用。", id);
                }
            }
        }
        for (Map.Entry<String, int[]> entry : byMod.entrySet()) {
            LOGGER.info("[飲食冷暖] 模組 {}：設定 {} 筆，未註冊 {} 筆。",
                    entry.getKey(), entry.getValue()[0], entry.getValue()[1]);
        }
        LOGGER.info("[飲食冷暖] 已載入 {} 筆食物溫度設定，{} 筆物品 ID 未註冊，{} 筆需進一步確認食用流程。",
                registry.size(), missing, needsConsumptionVerification);
    }
    @SubscribeEvent
    public void onFinishedUsing(LivingEntityUseItemEvent.Finish event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) return;
        String id = BuiltInRegistries.ITEM.getKey(event.getItem().getItem()).toString();
        if (!bridge.isConfigured(id)) return;
        // Some modded consumables implement a custom use flow without FOOD.
        // Require an eating/drinking animation for those; never trigger on
        // arbitrary completed item use such as tools or placeable blocks.
        boolean food = event.getItem().has(DataComponents.FOOD);
        UseAnim animation = event.getItem().getUseAnimation();
        boolean consumingAnimation = animation == UseAnim.EAT || animation == UseAnim.DRINK;
        if (!food && !consumingAnimation) return;
        // Detached/fake server players may complete item use without a server.
        // Match the TAN modifier guard and avoid dereferencing a null server.
        var server = player.getServer();
        if (server == null) return;
        bridge.consumed(player.getUUID(), id, server.getTickCount());
    }
    @SubscribeEvent
    public void onServerStopped(ServerStoppedEvent event) { bridge.clear(); }
    @SubscribeEvent
    public void onLogout(PlayerEvent.PlayerLoggedOutEvent event) {
        bridge.logout(event.getEntity().getUUID());
    }
}