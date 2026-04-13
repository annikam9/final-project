"""
data_processing.py
Loads and processes all CSV data for the defenders website.
Returns structured dicts ready to pass into the Jinja2 template.
"""

import pandas as pd
import json


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

LATAM_COUNTRIES = [
    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia",
    "Costa Rica", "Dominican Republic", "Ecuador", "Guatemala",
    "Honduras", "Mexico", "Nicaragua", "Panama", "Paraguay",
    "Peru", "Venezuela",
]

YEARS = list(range(2012, 2025))


# ─────────────────────────────────────────────
# LOADERS
# ─────────────────────────────────────────────

def load_defenders(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig", encoding_errors="replace")
    df["is_oc"] = df["involvement_perpetrator_type"].str.contains(
        "Organised crime", na=False
    )
    df["is_indigenous"] = df["person_characteristics"].str.contains(
        "Indigenous", na=False
    )
    df["is_oc_indigenous"] = df["is_oc"] & df["is_indigenous"]
    return df


def load_oc_index(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", encoding="latin-1", on_bad_lines="skip")
    df.columns = df.columns.str.strip()
    return df


# ─────────────────────────────────────────────
# PROCESSORS
# ─────────────────────────────────────────────

def _to_float(value) -> float | None:
    """Convert comma-decimal strings like '7,75' to float."""
    try:
        return round(float(str(value).replace(",", ".")), 2)
    except (ValueError, TypeError):
        return None


def build_country_stats(defenders: pd.DataFrame, oc: pd.DataFrame) -> dict:
    """
    Returns a dict keyed by country with dashboard stats.
    Used for Viz 1 (country dashboard).
    """
    latam = defenders[defenders["event_country"].isin(LATAM_COUNTRIES)]
    stats = {}

    for country in LATAM_COUNTRIES:
        df = latam[latam["event_country"] == country]
        if df.empty:
            stats[country] = None
            continue

        act_counts = df["act_type"].value_counts().to_dict()
        oc_row = oc[oc["Country"] == country]

        criminality = (
            _to_float(oc_row["Criminality avg."].values[0])
            if not oc_row.empty else None
        )
        resilience = (
            _to_float(oc_row["Resilience avg,"].values[0])
            if not oc_row.empty else None
        )

        stats[country] = {
            "total":               int(len(df)),
            "oc_share":            round(float(df["is_oc"].mean()) * 100, 1),
            "indigenous_share":    round(float(df["is_indigenous"].mean()) * 100, 1),
            "oc_indigenous_share": round(float(df["is_oc_indigenous"].mean()) * 100, 1),
            "murders":             int(act_counts.get("Murder", 0)),
            "disappearances":      int(act_counts.get("Disappearance", 0)),
            "criminality":         criminality,
            "resilience":          resilience,
            "attacks_2024":        int(len(df[df["year"] == 2024])),
        }

    return stats


def build_timeline(defenders: pd.DataFrame) -> dict:
    """
    Returns per-country, per-year data for Viz 3 (bar chart timeline).
    Keys: 'y' year, 't' total, 'oc' OC%, 'ind' indigenous%, 'oci' OC+indigenous%
    """
    latam = defenders[defenders["event_country"].isin(LATAM_COUNTRIES)]
    timeline = {}

    for country in LATAM_COUNTRIES:
        df = latam[latam["event_country"] == country]
        if df.empty:
            continue

        points = []
        for yr in YEARS:
            df_yr = df[df["year"] == yr]
            total = len(df_yr)
            points.append({
                "y":   yr,
                "t":   total,
                "oc":  round(float(df_yr["is_oc"].mean()) * 100, 1) if total else 0,
                "ind": round(float(df_yr["is_indigenous"].mean()) * 100, 1) if total else 0,
                "oci": round(float(df_yr["is_oc_indigenous"].mean()) * 100, 1) if total else 0,
            })
        timeline[country] = points

    return timeline


def build_world_data(defenders: pd.DataFrame) -> list:
    """
    Returns per-country totals for Viz 2 (world map).
    """
    agg = (
        defenders
        .groupby("event_country")
        .agg(
            total=("id", "count"),
            lat=("latitude", "first"),
            lon=("longitude", "first"),
            attacks_2024=("year", lambda x: int((x == 2024).sum())),
        )
        .reset_index()
        .rename(columns={"event_country": "country"})
    )
    # Ensure lat/lon are plain floats (not numpy types)
    agg["lat"] = agg["lat"].astype(float)
    agg["lon"] = agg["lon"].astype(float)
    return agg.to_dict(orient="records")


# ─────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────

def load_all(
    defenders_path: str,
    oc_path: str,
) -> dict:
    """
    Load and process all data.
    Returns a dict with JSON-serialisable strings for the template.
    """
    defenders = load_defenders(defenders_path)
    oc        = load_oc_index(oc_path)

    country_stats = build_country_stats(defenders, oc)
    timeline      = build_timeline(defenders)
    world_data    = build_world_data(defenders)

    return {
        "country_stats_json": json.dumps(country_stats,  ensure_ascii=False),
        "timeline_json":      json.dumps(timeline,       ensure_ascii=False),
        "world_data_json":    json.dumps(world_data,     ensure_ascii=False),
        "latam_countries":    LATAM_COUNTRIES,
    }
