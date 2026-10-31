package tw.zonezero.foodtemp;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
public final class PlayerThermalService {
    private final Map<UUID, ThermalAccumulator> states = new HashMap<>();
    public double onConsumed(UUID playerId, double foodTier, long gameTick) {
        if (foodTier == 0) return current(playerId, gameTick);
        return states.computeIfAbsent(playerId, id -> new ThermalAccumulator(gameTick)).consume(foodTier, gameTick);
    }
    public int modifierOffset(UUID playerId, long gameTick) {
        ThermalAccumulator state = states.get(playerId);
        if (state == null) return 0;
        int result = state.levelOffset(gameTick);
        if (state.value(gameTick) == 0.0) states.remove(playerId);
        return result;
    }
    public double current(UUID playerId, long gameTick) {
        ThermalAccumulator state = states.get(playerId);
        return state == null ? 0.0 : state.value(gameTick);
    }
    public void onLogout(UUID playerId) { states.remove(playerId); }
    public void clear() { states.clear(); }
    public int trackedPlayers() { return states.size(); }
}