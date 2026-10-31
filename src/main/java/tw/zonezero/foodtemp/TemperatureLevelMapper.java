package tw.zonezero.foodtemp;
public final class TemperatureLevelMapper {
    private TemperatureLevelMapper() {}
    public static int apply(int baseLevel, int offset) {
        if (baseLevel < 0 || baseLevel > 4) throw new IllegalArgumentException("baseLevel must be 0..4");
        if (offset < -1 || offset > 1) throw new IllegalArgumentException("offset must be -1..1");
        return Math.max(0, Math.min(4, baseLevel + offset));
    }
}