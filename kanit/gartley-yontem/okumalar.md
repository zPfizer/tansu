# Gartley yöntem: belirsiz kural okumaları (sınavdan önce donduruldu, 30.10.2026)

Bu okumalar `yontem.py` yazılırken seçildi ve bağımsız incelemede kabul edildi (sonuç: NOTLU GEÇTİ). Ayrık grup
sınavı bu okumalarla koşar. 12. madde Değişiklik 1 ile değişti: sahte oran sınamasında R/R kapısı kapalıdır.
Metin yazarın İngilizce raporundan aynen alındı.
1. Signal-level risk: the plan writes (entry - stop). I use the engine risk max(entry - stop, 0.5 ATR) because the engine defines R this way. The CSV also has `R_ham` = literal (entry - stop), and `taban_bagladi` marks rows where the floor applies (Gartley 2 rows; mean `R_ham` 1.142). Other candidates: 0 rows.
2. Signal-level costs: commission 0.1575 % and slippage 1 price tick (at least 0.1 %) on each side, with `para.Piyasa.kayma`.
3. Signal level ignores the open-trade rule ("her sinyal"). The money layer keeps the engine rule, as `para.py` does.
4. Trading day = a row with finite high, low, and close. The touch window counts rows t+1 to t+20, as the engine counts the 20-day order life. Confirmation window and time stop count trading days.
5. "Low <= X before t0" cannot occur without low <= D first, so it is implied. The break check runs from t0 to tc, tc included, because the intraday low comes before the confirming close.
6. tc is the first confirmation day. If the gate rejects tc, I do not search a later day.
7. AB=CD: the G-T break level "X" maps to the AB=CD stop (D - 2 ATR). "Price passes A" = high > A, checked from the day after C confirmation through tc. If high > A and low <= D fall on the same day, the setup drops. I also require B < C < A (D < B is then automatic).
8. Next-day market entry: the sizing price (`seviye`) is the tc close. `para.portfoy` sizes with `seviye`.
9. Two setups on the same tc: the higher D stays, as in `gartley.hesapla`.
10. Time stop: on the 10th trading day after the fill day, if no close from the fill day through that day reached hedef1, the exit is the next priced day at AOF (engine pending exit).
11. Pullback (`geri`): RSI(2) Wilder and SMA on trading days. Stop = fill price - 2 x ATR(14) of the signal day. The 3 ATR trail and the open-below-stop exit also apply, because plan "Ortak kurallar" puts them in the money layer.
12. Placebo: the R/R gate 1.4 stays ("diğer kurallar dondurulmuş Gartley ile aynı"). Percentile = share of valid draws with mean R strictly below Gartley.
13. Indicators: RSI = `gostergeler.rsi` (Wilder). ATR = `gostergeler.atr_basit` (the engine ATR).
14. Bootstrap: resample ISO weeks with replacement (same week count), mean of the pooled R. Seed 20261030.
15. Money-layer calendar and BIST 100 come from the symbols of the run (371 `ayar` symbols), not from all symbols.
16. Check 1 uses all 673 symbols because the brief requires the known 517,830.85 TL figure. It computes only the frozen Gartley, which the plan already lists as computed on all symbols. No new rule touches holdout symbols.
