import numpy as np
import pandas as pd

def divide_by_90(df):
    """
    Divides all numeric columns (except identifiers and playing time stats) 
    by the '90s' column to get Per 90 statistics.
    
    If '90s' column is missing, divides by 90.0 scalar.
    """
    # Create a copy to avoid SettingWithCopy warnings on the original df if desired, 
    # but user said "edit all", implying modification. 
    # We'll modify in place if possible or return modified.
    
    # Identify numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Columns to exclude from division
    # User excluded: league, team, player.
    # We also typically exclude metadata/playing time stats from normalization.
    exclude_sub_cols = ['MP', 'Starts', 'Min', '90s', 'age', 'born', 'league', 'team', 'player', 'season']
    
    cols_to_divide = []
    for col in numeric_cols:
        # Check if the column name (or second level if MultiIndex) is in exclusion list
        col_name = col[1] if isinstance(col, tuple) and len(col) > 1 else col
        if isinstance(col, tuple):
             # Also check level 0 just in case
             if col[0] in exclude_sub_cols:
                 continue
        
        if col_name not in exclude_sub_cols:
            cols_to_divide.append(col)
            
    # Find the divisor ('90s' played)
    divisor = None
    if ('Playing Time', '90s') in df.columns:
        divisor = df[('Playing Time', '90s')]
    elif '90s' in df.columns:
        divisor = df['90s']
    
    if divisor is not None:
        # Avoid division by zero by replacing 0 with NaN or inf? 
        # Pandas handles div by zero (results in inf).
        df[cols_to_divide] = df[cols_to_divide].div(divisor, axis=0)
    else:
        # Fallback to scalar 90 if no 90s column found (or if user strictly meant 90)
        df[cols_to_divide] = df[cols_to_divide] / 90.0
        
    return df
