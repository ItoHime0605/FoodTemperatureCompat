package tw.zonezero.foodtemp;
public final class ThermalAccumulator {
    private static final double MAX_ABS = 3.5;
    private static final long DECAY_TICKS_PER_POINT = 1200L;
    private double balance;
    private long lastTick;
    public ThermalAccumulator(long tick) { lastTick = tick; }
    public synchronized double value(long tick) {
        long elapsed = tick >= lastTick ? tick - lastTick : 0L;
        double decay = (double) elapsed / DECAY_TICKS_PER_POINT;
        balance = Math.copySign(Math.max(0, Math.abs(balance) - decay), balance);
        if (balance == 0.0) balance = 0.0; // Normalize negative zero for state cleanup.
        if (tick > lastTick) lastTick = tick;
        return balance;
    }
    public synchronized double consume(double tier, long tick) {
        if (!Double.isFinite(tier) || tier < -3 || tier > 3) throw new IllegalArgumentException("tier must be finite and within -3..3");
        value(tick);
        double strength = Math.abs(tier);
        // Preserve the previous integer-tier strengths exactly; interpolate fractional tiers.
        double delta = strength <= 1.0 ? 0.18 * strength
                : strength <= 2.0 ? 0.18 + (strength - 1.0) * 0.34
                : 0.52 + (strength - 2.0) * 0.43;
        if (tier != 0 && Math.signum(balance) == Math.signum(tier))
            delta *= 1.0 - Math.min(0.55, Math.abs(balance) / MAX_ABS * 0.55);
        balance = Math.max(-MAX_ABS, Math.min(MAX_ABS, balance + Math.signum(tier) * delta));
        return balance;
    }
    public synchronized int levelOffset(long tick) {
        double v = value(tick);
        return v >= 1.0 ? 1 : v <= -1.0 ? -1 : 0;
    }
}