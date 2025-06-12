"""Stress  testing utilities for the application."""

from typing import Dict, Literal
import pandas as pd
from utils.reconciliation import reconcile_trades

ShockType = Literal["price_pct", "qty_abs"]

def apply_shocks(df: pd.DataFrame,
                 shocks: Dict[str, Dict[ShockType, float]],
                 side: Literal["internal", "clearer"]) -> pd.DataFrame:
    """
    Return a *copy* of df with specified shocks applied month-by-month.

    Parameters
    ----------
    df      : internal or clearer table with columns ['month','quantity_mwh','price_eur_per_mwh']
    shocks  : {"2025-04": {"price_pct": +0.10, "qty_abs": -50}, ...}
    side    : 'internal' or 'clearer'  (just for logging / clarity)

    Notes
    -----
    • price_pct  = +0.10 means +10 % price jump  
    • qty_abs    = -50    means subtract 50 MWh from that month
    """
    out = df.copy(deep=True)

    for month, sdict in shocks.items():
        mask = out["month"] == month
        if not mask.any():
            print(f"[warn] {side}: month {month} not present, skipping")
            continue
        if "price_pct" in sdict:
            out.loc[mask, "price_eur_per_mwh"] *= (1 + sdict["price_pct"])
        if "qty_abs" in sdict:
            out.loc[mask, "quantity_mwh"] += sdict["qty_abs"]
    return out


# ------------------------------------------------------------------
# 2)  One-liner scenario runner
# ------------------------------------------------------------------
def run_scenario(internal_base: pd.DataFrame,
                 clearer_base : pd.DataFrame,
                 shocks_int   : Dict[str, Dict[ShockType, float]] | None = None,
                 shocks_clr   : Dict[str, Dict[ShockType, float]] | None = None
                 ) -> pd.DataFrame:
    """
    Apply shocks, reconcile, and return the diff table.
    """
    int_shocked = apply_shocks(internal_base, shocks_int or {}, side="internal")
    clr_shocked = apply_shocks(clearer_base , shocks_clr or {}, side="clearer")
    recon_tbl   = reconcile_trades(int_shocked, clr_shocked)
    return recon_tbl