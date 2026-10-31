package tw.zonezero.foodtemp;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.Reader;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;
public final class FoodTierRegistry {
    private static final Pattern ID = Pattern.compile("[a-z0-9_.-]+:[a-z0-9_./-]+");
    private Map<String, Double> tiers = Map.of();
    public synchronized int load(Reader input) throws IOException {
        Map<String, Double> next = new HashMap<>();
        try (BufferedReader lines = new BufferedReader(input)) {
            String line;
            int number = 0;
            while ((line = lines.readLine()) != null) {
                number++;
                String clean = line.split("#", 2)[0].trim();
                if (clean.isEmpty()) continue;
                int equals = clean.indexOf('=');
                if (equals < 0) throw new IOException("Missing '=' on line " + number);
                String id = clean.substring(0, equals).trim();
                if (!ID.matcher(id).matches()) throw new IOException("Invalid item ID on line " + number);
                double tier;
                try { tier = Double.parseDouble(clean.substring(equals + 1).trim()); }
                catch (NumberFormatException e) { throw new IOException("Invalid tier on line " + number, e); }
                if (!Double.isFinite(tier) || tier < -3 || tier > 3) throw new IOException("Tier outside -3..3 on line " + number);
                if (next.putIfAbsent(id, tier) != null) throw new IOException("Duplicate item ID on line " + number);
            }
        }
        tiers = Collections.unmodifiableMap(next);
        return next.size();
    }
    public boolean contains(String itemId) { return tiers.containsKey(itemId); }
    public double tier(String itemId) { return tiers.getOrDefault(itemId, 0.0); }
    public int size() { return tiers.size(); }
    /** Immutable snapshot for validation after all mods finish registering items. */
    public Map<String, Double> entries() { return tiers; }
}