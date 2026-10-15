Project folder: C:\Users\levent\Desktop\TANSU. Read-only. Do not change any file.
First action: read docs/KURALLAR.md and print its first line.

Rule (owner decision, KURALLAR "Okuma kuralları"): Tansu's ideas come first. A YORUM (our own choice) is valid only where Tansu has no idea on that point. If Tansu has an idea, our rule must follow it. If we cannot follow it (for example the data has no opening price), the reason is written ("uygulanamaz").
Special case: if Tansu explicitly leaves a detail to the reader or refuses to share it (for example "parametreleri veremem, siz detaylandırın"), that point counts as "Tansu sessiz".

Task:
1. List every YORUM and every point where our rules differ from Tansu in docs/KURALLAR.md, docs/TASARIM.md and docs/kurallar/A-yapi-bolge.md … E-risk-cikis-surec.md. Search for "YORUM", "bizim", "Tansu'nun ... yok", "kaynakta yok", and read §3 of KURALLAR and §5 of TASARIM fully. Include also these known points: same-sector pair rule; EMA squeeze entry after the squeeze ends vs Tansu's pre-signal during the squeeze; execution at next-day AOF vs Tansu's next-day open; next-day exit for the end-of-day stop; card states AKTİF/STOP/BOZULDU bound to positions; liquidity measure and cap; fixed parameters vs Tansu's walk-forward tuning; shock filter; Wilder smoothing in ATR; rounding quantity down to lot; log-price OLS for beta; names "acil stop" and "gün sonu stopu"; harmonic D target; cash until first entry in pairs; the word "bozulma".
2. For each point, search the Tansu pool for Tansu's own view: C:\Users\levent\Desktop\YONETIM\beyin\kisisel\300-Projects\Tansu X Veri Havuzu\ (notes and assets/ images). Use the source files that A–E cite first, then grep the pool. Open the image when the note may differ; the image wins. NotebookLM infographics are Tansu-shared but not his own tool; say so.
3. Classify each point as exactly one of:
   - SESSİZ: Tansu gives no idea, or explicitly leaves it to us → YORUM stays.
   - TANSU'YA ÇEVİR: Tansu has a clear idea and we can follow it → say exactly what our rule must become.
   - UYGULANAMAZ: Tansu has an idea but we cannot follow it → give the concrete reason.
   - BELİRSİZ: Tansu's idea exists but its reading is unclear → say what is unclear (this goes to the owner as a question).

Rules: every row needs our place (file:line) and Tansu's place (pool file:line or image path), both opened by you. Do not invent. Plain, short Turkish.

Output (Markdown):
## Ne okudum
## Tablo
| # | Nokta | Bizdeki yer | Bizim kural | Tansu'nun yeri | Tansu ne diyor | Sınıf | Ne olmalı |
## Belirsizler (sahibe soru)
## Boşluklar
