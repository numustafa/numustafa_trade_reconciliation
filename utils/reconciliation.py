"""Trade Reconciliation Utilities."""

from typing import List, Dict, Any
import pandas as pd

def convert_qtr_into_months(qtr_row: pd.Series,
                            start_trade_id: int = 1) -> pd.DataFrame:
    """
    Decompose one quarterly trade into three monthly legs.

    Parameters
    ----------
    qtr_row : pd.Series
        Row with keys ['quantity_mwh', 'price_eur_per_mwh'].
    start_trade_id : int, default 1
        First trade-id to assign to the decomposed legs.

    Returns
    -------
    pd.DataFrame
        One row per month with trade_id, contract_type, contract_period,
        quantity_mwh and price_eur_per_mwh.
    """
    # which months belong to the quarter (Q2-25 → Apr, May, Jun)
    months = ['2025-04', '2025-05', '2025-06']

    qty_per_month = qtr_row['quantity_mwh'] / len(months)
    price         = qtr_row['price_eur_per_mwh']

    rows = []
    for offset, month in enumerate(months):
        rows.append({
            'trade_id'          : start_trade_id + offset,
            'contract_type'     : 'Quarterly decomposed',
            'contract_period'   : month,
            'quantity_mwh'      : qty_per_month,
            'price_eur_per_mwh' : price
        })

    return pd.DataFrame(rows)


def add_monthly_legs_to_trades(trades: pd.DataFrame) -> pd.DataFrame:
    """
    Add monthly legs to trades by decomposing quarterly trades.

    Args:
        trades (pd.DataFrame): DataFrame containing quarterly trades.

    Returns:
        pd.DataFrame: DataFrame with monthly legs added.
    """
    monthly_legs = []
    for _, row in trades.iterrows():
        monthly_leg = convert_qtr_into_months(row)
        monthly_legs.append(monthly_leg)

    return pd.concat(monthly_legs, ignore_index=True)



def net_monthly_trades(trades: pd.DataFrame) -> pd.DataFrame:
    """
    Net monthly trades by summing up quantities of same months and take the average price.
    Args:
        trades (pd.DataFrame): DataFrame containing monthly trades.
    Returns:
        pd.DataFrame: DataFrame with net monthly trades.
    """
    # Get unique months from the contract_period column
    months = trades['contract_period'].unique()
    net_trades = []
    
    for month in months:
        # Filter trades for the current month 
        monthly_trades = trades[trades['contract_period'] == month]

        # Calculate total quantity and average price for the month
        total_quantity = monthly_trades['quantity_mwh'].sum()
        average_price = (monthly_trades['price_eur_per_mwh'] * monthly_trades['quantity_mwh']).sum() / total_quantity
        net_trade = {
            'contract_type': 'Net Monthly Trade',
            'contract_period': month,
            'quantity_mwh': total_quantity.astype(int),
            'price_eur_per_mwh': round(average_price,1)
        }
        net_trades.append(net_trade)
    return pd.DataFrame(net_trades)


def reconcile_trades(internal_trades: pd.DataFrame,
                     clearer_trades: pd.DataFrame) -> pd.DataFrame:
    """
    Reconcile internal trades with clearer trades.
    Args:
        internal_trades (pd.DataFrame): DataFrame containing internal trades.
        clearer_trades (pd.DataFrame): DataFrame containing clearer trades.
    Returns:
        pd.DataFrame: DataFrame with reconciled trades.
    """
    # Merge internal and clearer trades on month
    reconciliation = pd.merge(
        internal_trades[["month", "quantity_mwh", "price_eur_per_mwh"]],
        clearer_trades[["month", "quantity_mwh", "price_eur_per_mwh"]],
        on="month",
        suffixes=('_internal', '_clearer'),
        how='outer'
    )
    # Calculate differences
    reconciliation['quantity_diff'] = (reconciliation['quantity_mwh_internal'] -
                                       reconciliation['quantity_mwh_clearer']).fillna(0)

    reconciliation['price_diff'] = (reconciliation['price_eur_per_mwh_internal'] -
                                    reconciliation['price_eur_per_mwh_clearer']).fillna(0)

    # Reorder columns
    column_order = [
        'month',
        'quantity_mwh_internal',
        'quantity_mwh_clearer',
        'quantity_diff',
        'price_eur_per_mwh_internal',
        'price_eur_per_mwh_clearer',
        'price_diff'
    ]
    reconciliation = reconciliation[column_order]

    # Round the Numerical columns
    numerical_columns = [
        'quantity_mwh_internal',
        'quantity_mwh_clearer',
        'quantity_diff',
        'price_eur_per_mwh_internal',
        'price_eur_per_mwh_clearer',
        'price_diff'
    ]
    for col in numerical_columns:
        reconciliation[col] = reconciliation[col].round(2)
    
    final = reconciliation.sort_values(by='month').reset_index(drop=True)
    return final


def print_reconciliation_summary(reconciliation: pd.DataFrame) -> None:
    """
    Print a summary of the reconciliation results.
    Args:
        reconciliation (pd.DataFrame): DataFrame containing reconciliation results.
    """
    print("Reconciliation Summary:")
    print(reconciliation)
    print("\nTotal Trades Reconciled:", len(reconciliation))
    print("Total Quantity Mismatches:", reconciliation['quantity_diff'].abs().sum())
    print("\nTotal Quantity Difference:", reconciliation['quantity_diff'].sum())
    print("Total Price Difference:", reconciliation['price_diff'].sum())
    print("\nReconciliation completed successfully.")




