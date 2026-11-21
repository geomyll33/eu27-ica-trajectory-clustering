"""
Υπολογισμός Περιφερειακού Δείκτη Κατά Κεφαλήν ΑΕΠ σε PPS (2015–2017, EU-27 = 100)
1. Κατεβάζει το demo_r_d2jan (πληθυσμός 1ης Ιανουαρίου, NUTS 2, έτη 2015–2017) στον τρέχοντα φάκελο
2. Κατεβάζει το nama_10r_2gdp (unit=PPS_EU27_2020_HAB, 2015–2017) στον τρέχοντα φάκελο
3. Υπολογίζει για κάθε περιφέρεια NUTS 2:
   - Απόλυτο ΑΕΠ σε PPS (2015–2017) = Σ (PPS_EU27_2020_HAB_t × Πληθυσμός_t)
   - Κατά κεφαλήν ΑΕΠ PPS (2015–2017) = Απόλυτο ΑΕΠ PPS (2015–2017) ÷ Σ Πληθυσμός_t
4. Υπολογίζει τον μέσο όρο ΕΕ-27 (2015–2017) = Σύνολο ΑΕΠ PPS ΕΕ-27 ÷ Σύνολο Πληθυσμού ΕΕ-27
5. Υπολογίζει τον Δείκτη Περιφέρειας = (Κατά κεφαλήν ΑΕΠ 2015–2017 ÷ Μέσος όρος ΕΕ-27) × 100
   και αποθηκεύει το αποτέλεσμα στο nuts2_gdp_pps_index_2015_2017.csv

Απαιτείται: pip install pandas requests
"""

import io
import pandas as pd
import requests

YEARS = [2015, 2016, 2017]
EU27_COUNTRIES = {
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES",
    "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
    "NL", "PL", "PT", "RO", "SE", "SI", "SK"
}

# SDMX 2.1 URLs της Eurostat
# demo_r_d2jan διαστάσεις: FREQ . UNIT . SEX . AGE . GEO
URL_POP = (
    "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/"
    "DEMO_R_D2JAN/A.NR.T.TOTAL.?format=SDMX-CSV&startPeriod=2015&endPeriod=2017"
)

# nama_10r_2gdp διαστάσεις: FREQ . UNIT . GEO
URL_GDP = (
    "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/"
    "NAMA_10R_2GDP/A.PPS_EU27_2020_HAB.?format=SDMX-CSV&startPeriod=2015&endPeriod=2017"
)


def fetch_sdmx_csv(url: str, save_path: str) -> pd.DataFrame:
    print(f"Λήψη από Eurostat -> {save_path} ...")
    r = requests.get(url, timeout=90)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.to_csv(save_path, index=False)
    print(f"  -> Αποθηκεύτηκε ({len(df)} γραμμές)")
    return df


def main():
    # 1. Λήψη πληθυσμού (demo_r_d2jan, 2015–2017)
    pop_path = "demo_r_d2jan_2015_2017.csv"
    df_pop_raw = fetch_sdmx_csv(URL_POP, pop_path)

    # 2. Λήψη ΑΕΠ κατά κάτοικο PPS (nama_10r_2gdp, PPS_EU27_2020_HAB, 2015–2017)
    gdp_path = "nama_10r_2gdp_pps_2015_2017.csv"
    df_gdp_raw = fetch_sdmx_csv(URL_GDP, gdp_path)

    # Καθαρισμός και φιλτράρισμα στηλών
    pop = df_pop_raw[["geo", "TIME_PERIOD", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "pop"})
    gdp = df_gdp_raw[["geo", "TIME_PERIOD", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "gdp_pc_pps"})

    pop["TIME_PERIOD"] = pd.to_numeric(pop["TIME_PERIOD"], errors="coerce")
    gdp["TIME_PERIOD"] = pd.to_numeric(gdp["TIME_PERIOD"], errors="coerce")
    pop["pop"] = pd.to_numeric(pop["pop"], errors="coerce")
    gdp["gdp_pc_pps"] = pd.to_numeric(gdp["gdp_pc_pps"], errors="coerce")

    pop = pop[pop["TIME_PERIOD"].isin(YEARS)].dropna(subset=["pop"])
    gdp = gdp[gdp["TIME_PERIOD"].isin(YEARS)].dropna(subset=["gdp_pc_pps"])

    # Κρατάμε μόνο χώρες/περιφέρειες της ΕΕ-27
    pop["country"] = pop["geo"].astype(str).str[:2]
    gdp["country"] = gdp["geo"].astype(str).str[:2]
    pop = pop[pop["country"].isin(EU27_COUNTRIES)].copy()
    gdp = gdp[gdp["country"].isin(EU27_COUNTRIES)].copy()

    # Ένωση ανά (geo, TIME_PERIOD)
    merged = pd.merge(gdp, pop, on=["geo", "country", "TIME_PERIOD"], how="inner")
    merged["gdp_total_pps"] = merged["gdp_pc_pps"] * merged["pop"]

    # --- Βήμα 3: Μέσος όρος ΕΕ-27 περιόδου 2015–2017 ---
    eu27_countries_df = merged[merged["geo"].astype(str).str.len() == 2].copy()
    if eu27_countries_df["country"].nunique() == 27:
        eu27_total_gdp = eu27_countries_df["gdp_total_pps"].sum()
        eu27_total_pop = eu27_countries_df["pop"].sum()
    else:
        nuts2_fallback = merged[merged["geo"].astype(str).str.len() == 4]
        eu27_total_gdp = nuts2_fallback["gdp_total_pps"].sum()
        eu27_total_pop = nuts2_fallback["pop"].sum()

    eu27_avg_pc_pps = eu27_total_gdp / eu27_total_pop
    print(f"\nΜέσος όρος ΕΕ-27 (2015–2017): {eu27_avg_pc_pps:,.2f} PPS / κάτοικο")

    # --- Βήματα 2 & 4: Υπολογισμός ανά περιφέρεια NUTS 2 (len(geo) == 4) ---
    nuts2 = merged[merged["geo"].astype(str).str.len() == 4].copy()

    reg_agg = (
        nuts2.groupby(["country", "geo"], as_index=False)
        .agg(
            years_count=("TIME_PERIOD", "count"),
            gdp_total_pps_2015_2017=("gdp_total_pps", "sum"),
            pop_total_2015_2017=("pop", "sum"),
        )
    )

    reg_agg["gdp_pc_pps_2015_2017"] = (
        reg_agg["gdp_total_pps_2015_2017"] / reg_agg["pop_total_2015_2017"]
    )

    reg_agg["eu27_avg_pc_pps_2015_2017"] = eu27_avg_pc_pps
    reg_agg["regional_index_eu27_100"] = (
        reg_agg["gdp_pc_pps_2015_2017"] / eu27_avg_pc_pps
    ) * 100.0

    reg_agg = reg_agg.sort_values(["country", "geo"]).reset_index(drop=True)
    out_file = "nuts2_gdp_pps_index_2015_2017.csv"
    reg_agg.to_csv(out_file, index=False)

    print(f"Αποθηκεύτηκε ο τελικός πίνακας: {out_file} ({len(reg_agg)} περιφέρειες NUTS 2)")
    incomplete = reg_agg[reg_agg["years_count"] < 3]
    if not incomplete.empty:
        print(f"Προσοχή: {len(incomplete)} περιφέρειες έχουν <3 έτη δεδομένων: {incomplete['geo'].tolist()}")
    print("\nΔείγμα πρώτων 10 περιφερειών:")
    print(reg_agg[["geo", "years_count", "gdp_pc_pps_2015_2017", "regional_index_eu27_100"]].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
