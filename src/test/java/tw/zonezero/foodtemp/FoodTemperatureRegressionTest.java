package tw.zonezero.foodtemp;

import java.io.IOException;
import java.io.StringReader;

/**
 * 無需 Minecraft 或測試框架的純 Java 回歸測試。
 * 執行：./gradlew testClasses 後使用 java -cp build/classes/java/main:build/classes/java/test
 * tw.zonezero.foodtemp.FoodTemperatureRegressionTest
 */
public final class FoodTemperatureRegressionTest {
    private FoodTemperatureRegressionTest() {}

    private static void check(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }

    private static void registryDecimalsAndDuplicates() throws Exception {
        FoodTierRegistry registry = new FoodTierRegistry();
        int count = registry.load(new StringReader(
                "# 溫度測試\nexample:cheese_ball=0.5\nexample:chilled_mousse=-0.2\n"));
        check(count == 2, "小數設定數量錯誤");
        check(registry.tier("example:cheese_ball") == 0.5, "正小數讀取錯誤");
        check(registry.tier("example:chilled_mousse") == -0.2, "負小數讀取錯誤");
        check(registry.tier("example:neutral") == 0.0, "未設定物品應中性");
        try {
            registry.load(new StringReader("example:duplicate=1\nexample:duplicate=2\n"));
            throw new AssertionError("重複 ID 應遭拒絕");
        } catch (IOException expected) {
            check(registry.size() == 2, "讀取失敗不可破壞原設定");
        }
    }

    private static void accumulationAndDecay() {
        ThermalAccumulator accumulator = new ThermalAccumulator(0);
        check(accumulator.consume(0.5, 0) > 0, "高能量食品應累積少量暖意");
        check(accumulator.levelOffset(0) == 0, "單次 +0.5 不應直接提升 TAN 階級");
        for (int i = 0; i < 30; i++) accumulator.consume(3, 0);
        check(accumulator.levelOffset(0) == 1, "連續熱食應達到一階升溫");
        check(accumulator.value(12000) == 0.0, "長時間後應衰減至零");
        check(accumulator.levelOffset(12000) == 0, "衰減後不應殘留體溫階級");
        ThermalAccumulator cold = new ThermalAccumulator(0);
        cold.consume(-0.2, 0);
        check(cold.value(0) < 0, "冷藏甜點應累積少量冷意");
        check(cold.levelOffset(0) == 0, "單次 -0.2 不應直接降低 TAN 階級");
    }

    private static void clampTanLevel() {
        check(TemperatureLevelMapper.apply(0, -1) == 0, "低溫邊界溢出");
        check(TemperatureLevelMapper.apply(4, 1) == 4, "高溫邊界溢出");
        check(TemperatureLevelMapper.apply(2, 1) == 3, "升溫方向錯誤");
        check(TemperatureLevelMapper.apply(2, -1) == 1, "降溫方向錯誤");
    }

    public static void main(String[] args) throws Exception {
        registryDecimalsAndDuplicates();
        accumulationAndDecay();
        clampTanLevel();
        System.out.println("飲食冷暖：純 Java 回歸測試通過");
    }
}
