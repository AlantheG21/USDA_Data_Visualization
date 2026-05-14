# What's Really in Our Food?
## Nutritional Patterns Across the USDA SR Legacy Dataset

**Alan Garcia | CS 4379G — Data Analysis and Visualization | Texas State University | Spring 2026**

*This analysis is designed for a general audience curious about how foods compare nutritionally — no prior knowledge of nutrition science or data analysis is required.*

---

## Section 1 — The Question

Walk into any grocery store and the sheer variety of food is overwhelming. Nutrition labels exist to help, but they are dense with numbers that are hard to compare across products and categories. What if we could step back and ask a simpler question: **do foods naturally group into distinct nutritional types, and if so, what separates them?**

This project investigates nutritional patterns across 7,793 foods drawn from the USDA's Standard Reference (SR Legacy) database — one of the most comprehensive publicly available records of what American foods are made of. Using seven key nutrients per food, we ask:

- How do foods cluster by their macronutrient makeup — protein, fat, carbohydrates, sugar, fiber, sodium, and calories?
- What nutritional signatures separate whole foods from ultra-processed ones?
- Can we reduce thousands of foods to a small number of meaningful nutritional archetypes?

Understanding these patterns matters because dietary choices are one of the most controllable factors in long-term health outcomes, yet most people navigate food decisions without a clear map of the nutritional landscape. This analysis aims to make that map visible.

---

## Section 2 — The Data

**Source:** USDA FoodData Central — SR Legacy Dataset (2019 release).
Available at: [fdc.nal.usda.gov](https://fdc.nal.usda.gov/download-datasets)

The SR Legacy dataset covers 7,793 foods across 25 categories — from beef products and baked goods to fruits, vegetables, nuts, and beverages. It reports nutrient amounts per 100 grams of food, making every item directly comparable regardless of typical portion size.

**What we selected:** From hundreds of available nutrients, 15 were chosen to capture the core nutritional fingerprint of each food: protein, total fat, carbohydrates, fiber, total sugars, energy (calories), sodium, calcium, iron, cholesterol, saturated fat, and four vitamins (A, C, D, B12).

**How the data was cleaned:**

The four raw files (foods, nutrients, food-nutrient measurements, and categories) were merged and reshaped from a long format — one row per food-nutrient pair — into a wide format where each food becomes a single row with all its nutrient values as columns.

Missing nutrient measurements were handled by first identifying *why* each nutrient was missing, not simply dropping or filling blindly:

- **Biologically negligible values (e.g., Vitamin C in meats, Vitamin B12 in plant foods, cholesterol in vegetables)** were treated as true zeros. These nutrients are not reported for certain food types because they are genuinely absent — not because the measurement was skipped. Filling these with zero is the scientifically correct treatment.
- **Nutrients missing due to incomplete lab testing** (e.g., fiber or calcium not measured for some foods) were filled using the median value of other foods in the same category. This preserves the full dataset while using the most reasonable available estimate.

Dropping all foods with any missing value — a common shortcut — would have removed a disproportionate number of whole foods and raw ingredients, which tend to have fewer lab measurements than commercially packaged products with mandatory nutrition labels. This would have biased the analysis toward processed foods.

After cleaning, all 7,793 foods were retained with no incomplete records.

---

## Section 3 — Key Findings

**1. Fat is the primary driver of caloric density** *(VIZ-4, VIZ-5)*

Across all 7,793 foods, the correlation between total fat and calorie content is the strongest relationship in the dataset. The scatter plot of fat versus energy (VIZ-5) shows an almost perfectly linear relationship — foods like oils, butter, and nuts sit in the upper right corner with high fat and high calories, while vegetables and broths cluster near the origin with minimal fat and minimal calories. This means that for most foods, knowing the fat content alone gives a very reliable estimate of calorie density.

**2. Sodium is the clearest marker of ultra-processed foods** *(VIZ-3, VIZ-8)*

The top 20 highest-sodium foods (VIZ-8) are dominated by dry soup and bouillon powders, leavening agents (baking soda and baking powder), dry seasoning and gravy mixes, and pure salt — all exceeding 5,000 mg per 100 grams. Cured meats are elevated in sodium but do not appear in the top 20 because their water content dilutes concentration; these top entries are powders or near-pure compounds. The category-level box plot (VIZ-3) confirms the broader pattern: sausages and luncheon meats, soups, and fast foods have sodium levels five to ten times higher than whole-food categories. Sodium is not just a health concern — it is a reliable fingerprint for industrial food processing.

**3. Sugar and fiber separate sweets from vegetables** *(VIZ-7)*

The scatter plot of total sugars versus fiber (VIZ-7) shows that sweets span a wide range of sugar values but remain consistently near zero fiber, while most vegetables cluster in the low-sugar, low-fiber region — with a subset of higher-fiber vegetables appearing as outliers along the fiber axis. The clearest separation between the two categories is on fiber: no sweet food reaches meaningful fiber levels, while the highest-fiber items in the chart are exclusively vegetables. This pattern matters because fiber and sugar have opposing effects on how quickly the body processes carbohydrates — and the near-complete absence of fiber in sweets, regardless of their sugar content, is a reliable nutritional signature of ultra-processed foods.

**4. Animal-based categories dominate protein content** *(VIZ-2, EDA-11)*

The three food categories with the highest median protein per 100 grams are all animal-derived: beef products (24.2g), poultry products (23.4g), and lamb, veal, and game products (22.9g). The box plot in VIZ-2, sorted by median protein, makes the divide between animal and plant categories immediately visible. Plant-based categories do appear in the upper half — legumes and nut products carry meaningful protein — but no plant category reaches the consistent levels of the top three.

**5. Macro composition varies dramatically by category** *(VIZ-6)*

The stacked bar chart of average macro splits (VIZ-6) shows that different food categories are nutritionally dominated by entirely different macronutrients. Fats and oils are nearly 100% fat. Sweets and cereals are predominantly carbohydrates. Meats and poultry are primarily protein. Very few categories show a balanced split across all three macronutrients, which reinforces the idea that foods naturally fall into nutritional archetypes rather than existing on a uniform continuum.

---

## Section 4 — Nutritional Clusters

Using a mathematical grouping technique applied to the seven core nutrients, the 7,793 foods sorted themselves into seven distinct nutritional archetypes. Rather than relying on USDA category labels, this grouping is driven entirely by nutrient similarity — two foods end up in the same cluster only if their actual nutrient profiles are close, regardless of what category they belong to. The quality of this grouping was evaluated and found to be strong, meaning the seven groups are genuinely distinct from one another.

Here is what each group looks like in plain terms:

| Cluster | What it is | Typical foods |
|---------|-----------|---------------|
| **Low-Calorie Whole Foods** | Low in everything — protein, fat, carbs, and calories (avg 78 kcal/100g) | Raw vegetables, fruits, plain broths, water-based beverages |
| **Animal Proteins** | High protein (avg 23g/100g), very low carbohydrates | Meats, poultry, fish, eggs, plain dairy |
| **Calorie-Dense Fats & Oils** | Extremely high fat (avg 72g/100g) and calories (avg 694 kcal/100g) | Cooking oils, butter, lard, full-fat nuts |
| **Extreme Sodium Outliers** | Average sodium of 25,880 mg/100g — a statistical extreme with only 8 foods | Table salt, curing salts, pure seasoning concentrates |
| **High-Fiber Legumes & Seeds** | Highest fiber of any group (avg 26g/100g) with meaningful protein | Dried beans, lentils, seeds, high-fiber grains |
| **Processed Grains & Breads** | High carbohydrates, moderate fiber, elevated sodium | Cereals, bread, baked goods, pasta |
| **Sweets & Sugary Foods** | High carbohydrates (avg 67g/100g) with very high sugar (avg 50g/100g) | Candy, pastries, sweetened beverages, desserts |

The most interesting finding from the clustering is that the groups **cut across USDA categories**. The "Processed Grains & Breads" cluster, for example, draws from the baked products, cereals, snacks, and fast foods categories simultaneously — because they share a similar nutrient profile even though they appear in different sections of the grocery store. This suggests that a nutrient-based view of food reveals structure that the standard category system misses.

---

## Section 5 — Limitations

**Missing values are imputed, not measured.** While we used a principled approach to fill missing nutrient values rather than dropping foods, imputed values are estimates — not lab measurements. Foods whose fiber, calcium, or sodium values were filled using category medians may not perfectly reflect the actual food. This affects a minority of records but should be noted when interpreting results for specific foods.

**The dataset reflects 2019, not today.** The SR Legacy dataset was frozen at its 2019 release. Foods reformulated since then — for example, products that have reduced sodium or added fiber in response to consumer demand — are not captured here. Findings about processed food categories in particular may understate recent improvements by manufacturers.

**All values are per 100 grams, not per serving.** A 100-gram reference makes foods mathematically comparable, but it can be misleading in practice. A tablespoon of olive oil weighs about 14 grams — so its per-100g calorie count of 884 kcal looks alarming, but a typical portion contributes far less. Conversely, a 100g serving of breakfast cereal is larger than most people eat. The analysis describes the nutritional character of foods, not the dietary impact of typical portions.

**The "Extreme Sodium Outliers" cluster contains only 8 foods.** This group — table salt and concentrated seasoning products — is a mathematical outlier rather than a meaningful nutritional category. Its presence illustrates that k-means clustering is sensitive to extreme values and that domain knowledge is needed to interpret results appropriately.

**Cluster boundaries are not fixed.** The seven clusters represent a useful simplification, not a biological law. Many foods sit near the boundary between two groups — a lightly salted nut mix, for example, shares properties with both the "High-Fiber Legumes & Seeds" and "Calorie-Dense Fats & Oils" clusters. The clusters are a tool for exploration, not a definitive classification system.
