package tw.zonezero.foodtemp;
import toughasnails.api.temperature.IPlayerTemperatureModifier;
import toughasnails.api.temperature.TemperatureHelper;
import toughasnails.api.temperature.TemperatureLevel;
import net.minecraft.world.entity.player.Player;
public final class TanTemperatureAdapter implements IPlayerTemperatureModifier {
    private final ConsumptionBridge bridge;
    public TanTemperatureAdapter(ConsumptionBridge bridge) { this.bridge = bridge; }
    public static void register(ConsumptionBridge bridge) {
        TemperatureHelper.registerPlayerTemperatureModifier(new TanTemperatureAdapter(bridge));
    }
    @Override public TemperatureLevel modify(Player player, TemperatureLevel current) {
        if (player.level().isClientSide()) return current;
        int offset = bridge.temperatureOffset(player.getUUID(), player.getServer().getTickCount());
        return TemperatureLevel.values()[TemperatureLevelMapper.apply(current.ordinal(), offset)];
    }
}