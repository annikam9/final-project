"""
data_processing.py  —  load and process all CSV data for the defenders website.
"""
import json
from collections import Counter
import pandas as pd

LATAM_COUNTRIES = [
    "Argentina","Bolivia","Brazil","Chile","Colombia","Costa Rica",
    "Dominican Republic","Ecuador","Guatemala","Honduras","Mexico",
    "Nicaragua","Panama","Paraguay","Peru","Venezuela",
]
YEARS = list(range(2012, 2025))

PERP_LABELS = {
    "Organised crime / mafias":"Organised crime","Hitmen":"Hitmen",
    "Unknown":"Unknown","Police":"Police","Armed forces":"Armed forces",
    "Government officials/entities":"Gov. officials","Corporations":"Corporations",
    "Private military actors":"Private military","Landowners":"Landowners",
    "Private security guards":"Private security","Others":"Others","Poachers":"Poachers",
}
PERP_COLORS = {
    "Organised crime / mafias":"#e74c3c","Hitmen":"#c0392b","Unknown":"#555",
    "Police":"#2980b9","Armed forces":"#1a5276","Government officials/entities":"#8e44ad",
    "Corporations":"#d35400","Private military actors":"#7f8c8d","Landowners":"#27ae60",
    "Private security guards":"#16a085","Others":"#444","Poachers":"#f39c12",
}

def _f(v):
    try: return round(float(str(v).replace(",",".")), 2)
    except: return None

def load_defenders(path):
    df = pd.read_csv(path, encoding="utf-8-sig", encoding_errors="replace")
    df["is_oc"]         = df["involvement_perpetrator_type"].str.contains("Organised crime", na=False)
    df["is_indigenous"] = df["person_characteristics"].str.contains("Indigenous", na=False)
    df["is_oc_ind"]     = df["is_oc"] & df["is_indigenous"]
    return df

def load_oc(path):
    df = pd.read_csv(path, sep=";", encoding="latin-1", on_bad_lines="skip")
    df.columns = df.columns.str.strip()
    return df

def build_country_stats(defenders, oc23, oc25):
    latam = defenders[defenders["event_country"].isin(LATAM_COUNTRIES)]
    stats = {}
    for c in LATAM_COUNTRIES:
        df = latam[latam["event_country"] == c]
        if df.empty: stats[c] = None; continue
        acts = df["act_type"].value_counts().to_dict()
        r23 = oc23[oc23["Country"] == c]
        cr_col23 = [x for x in oc23.columns if "riminality avg" in x][0]
        res_col23 = [x for x in oc23.columns if "esilience" in x][0]
        stats[c] = {
            "total":               int(len(df)),
            "oc_share":            round(float(df["is_oc"].mean())*100, 1),
            "indigenous_share":    round(float(df["is_indigenous"].mean())*100, 1),
            "oc_indigenous_share": round(float(df["is_oc_ind"].mean())*100, 1),
            "murders":             int(acts.get("Murder", 0)),
            "disappearances":      int(acts.get("Disappearance", 0)),
            "attacks_2024":        int(len(df[df["year"]==2024])),
        }
    return stats

def build_oci_data(oc23, oc25):
    cr23 = [x for x in oc23.columns if "riminality avg" in x][0]
    re23 = [x for x in oc23.columns if "esilience" in x][0]
    cr25 = [x for x in oc25.columns if "riminality avg" in x][0]
    re25 = [x for x in oc25.columns if "esilience" in x][0]
    data = {}
    for c in LATAM_COUNTRIES:
        r23 = oc23[oc23["Country"]==c]
        r25 = oc25[oc25["Country"]==c]
        data[c] = {
            "c23": _f(r23[cr23].values[0]) if not r23.empty else None,
            "r23": _f(r23[re23].values[0]) if not r23.empty else None,
            "c25": _f(r25[cr25].values[0]) if not r25.empty else None,
            "r25": _f(r25[re25].values[0]) if not r25.empty else None,
        }
    return data

def build_perp_data(defenders):
    latam = defenders[defenders["event_country"].isin(LATAM_COUNTRIES)]
    data = {}
    for c in LATAM_COUNTRIES:
        df = latam[latam["event_country"]==c]
        if df.empty: continue
        counts = Counter()
        for v in df["involvement_perpetrator_type"].dropna():
            for p in str(v).split(","):
                p = p.strip()
                if p: counts[p] += 1
        total = sum(counts.values())
        data[c] = [
            {"label": PERP_LABELS.get(p,p), "count": n,
             "pct": round(n/total*100, 1) if total else 0,
             "color": PERP_COLORS.get(p,"#666")}
            for p,n in counts.most_common(5)
        ]
    return data

def build_timeline(defenders):
    latam = defenders[defenders["event_country"].isin(LATAM_COUNTRIES)]
    tl = {}
    for c in LATAM_COUNTRIES:
        df = latam[latam["event_country"]==c]
        if df.empty: continue
        pts = []
        for yr in YEARS:
            dy = df[df["year"]==yr]
            tot = len(dy)
            oc_n   = int(dy["is_oc"].sum())
            ind_n  = int(dy["is_indigenous"].sum())
            oci_n  = int(dy["is_oc_ind"].sum())
            oc_only  = int((dy["is_oc"] & ~dy["is_indigenous"]).sum())
            ind_only = int((~dy["is_oc"] & dy["is_indigenous"]).sum())
            both     = int(dy["is_oc_ind"].sum())
            neither  = tot - oc_only - ind_only - both
            pts.append({"y":yr,"t":tot,
                "oc_n":oc_n,"ind_n":ind_n,"oci_n":oci_n,
                "oc_only":oc_only,"ind_only":ind_only,"both":both,"neither":neither,
                "oc_pct":  round(oc_n/tot*100,1) if tot else 0,
                "ind_pct": round(ind_n/tot*100,1) if tot else 0,
                "oci_pct": round(oci_n/tot*100,1) if tot else 0})
        tl[c] = pts
    return tl

def build_world_data(defenders):
    agg = (defenders.groupby("event_country")
           .agg(total=("id","count"), lat=("latitude","first"), lon=("longitude","first"),
                attacks_2024=("year", lambda x: int((x==2024).sum())))
           .reset_index().rename(columns={"event_country":"country"}))
    agg["lat"] = agg["lat"].astype(float)
    agg["lon"] = agg["lon"].astype(float)
    return agg.to_dict(orient="records")

def load_all(defenders_path, oc23_path, oc25_path):
    defenders = load_defenders(defenders_path)
    oc23 = load_oc(oc23_path)
    oc25 = load_oc(oc25_path)
    return {
        "country_stats_json": json.dumps(build_country_stats(defenders, oc23, oc25), ensure_ascii=False),
        "oci_data_json":      json.dumps(build_oci_data(oc23, oc25),                ensure_ascii=False),
        "perp_data_json":     json.dumps(build_perp_data(defenders),                ensure_ascii=False),
        "timeline_json":      json.dumps(build_timeline(defenders),                  ensure_ascii=False),
        "world_data_json":    json.dumps(build_world_data(defenders),                ensure_ascii=False),
        "latam_countries":    LATAM_COUNTRIES,
    }
