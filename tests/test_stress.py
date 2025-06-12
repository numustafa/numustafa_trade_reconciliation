import sys
import os
import pandas as pd
from pytest import approx

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.stress import apply_shocks

def test_price_shock_up():
    df = pd.DataFrame(
        {"month": ["2025-04"],
         "quantity_mwh": [100.0],
         "price_eur_per_mwh": [30.0]}
    )
    shocked = apply_shocks(
        df,
        {"2025-04": {"price_pct": +0.10}},
        side="internal"
    )
    assert shocked.loc[0, "price_eur_per_mwh"] == approx(33.0, rel=1e-12)

