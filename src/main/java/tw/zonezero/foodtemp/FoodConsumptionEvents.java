package tw.zonezero.foodtemp;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.entity.living.LivingEntityUseItemEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
public final class FoodConsumptionEvents {
    private final ConsumptionBridge bridge;
    public FoodConsumptionEvents(ConsumptionBridge bridge) { this.bridge = bridge; }
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