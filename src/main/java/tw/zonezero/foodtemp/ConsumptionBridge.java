package tw.zonezero.foodtemp;
import java.util.UUID;
public final class ConsumptionBridge {
    private final FoodTierRegistry registry;
    private final PlayerThermalService service;
    public ConsumptionBridge(FoodTierRegistry registry, PlayerThermalService service) {
        this.registry = registry;
        this.service = service;
    }
    public boolean isConfigured(String itemId) { return registry.contains(itemId); }
    public double consumed(UUID player, String itemId, long tick) {
        return service.onConsumed(player, registry.tier(itemId), tick);
    }
    public int temperatureOffset(UUID player, long tick) {
        return service.modifierOffset(player, tick);
    }
    public void clear() { service.clear(); }
    public void logout(UUID player) { service.onLogout(player); }
}