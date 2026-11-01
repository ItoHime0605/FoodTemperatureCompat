package tw.zonezero.foodtemp;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
@Mod(FoodTemperatureCompatMod.MOD_ID)
public final class FoodTemperatureCompatMod {
    public static final String MOD_ID = "foodtemperaturecompat";
    private static final FoodTierRegistry REGISTRY = new FoodTierRegistry();
    private static final PlayerThermalService THERMAL = new PlayerThermalService();
    private static final ConsumptionBridge BRIDGE = new ConsumptionBridge(REGISTRY, THERMAL);
    public FoodTemperatureCompatMod() {
        try (var resource = getClass().getResourceAsStream("/food_temperature_tiers.txt")) {
            if (resource == null) throw new IllegalStateException("Missing food_temperature_tiers.txt");
            REGISTRY.load(new InputStreamReader(resource, StandardCharsets.UTF_8));
        } catch (IOException ex) { throw new IllegalStateException("Failed to load food tiers", ex); }
        TanTemperatureAdapter.register(BRIDGE);
        NeoForge.EVENT_BUS.register(new FoodConsumptionEvents(BRIDGE, REGISTRY));
        NeoForge.EVENT_BUS.register(new FoodTemperatureTooltip(REGISTRY));
    }
}