import os
import pandas as pd

def inspect_datasets(data_dir="data/raw"):
    """Loads all CSV files in the directory and prints diagnostic metrics."""
    if not os.path.exists(data_dir):
        print(f"Directory '{data_dir}' not found.")
        return {}

    # Read all CSVs (both the live ones you fetched and local ones you drop in later)
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    dfs = {}

    print(f"=== Found {len(csv_files)} CSV datasets in tracking ===")
    for file in csv_files:
        path = os.path.join(data_dir, file)
        name = os.path.splitext(file)[0]
        
        try:
            df = pd.read_csv(path)
            dfs[name] = df
            
            print("\n" + "="*40)
            print(f"Dataset: {file}")
            print("="*40)
            print(f"• Shape: {df.shape}")
            print("\n• Data Types:")
            print(df.dtypes)
            print("\n• Head:")
            print(df.head(2))
            
            # Basic Anomaly Quick-Check
            missing = df.isnull().sum().sum()
            dupes = df.duplicated().sum()
            if missing > 0 or dupes > 0:
                print(f"\n⚠️ Alert: Found {missing} missing values and {dupes} duplicate rows.")
                
        except Exception as e:
            print(f"❌ Error reading {file}: {e}")
            
    return dfs

def validate_amfi_codes(dfs):
    """Validates structural matching between fund master and history logs."""
    print("\n" + "="*50)
    print("DATA QUALITY SUMMARY: AMFI CODE VALIDATION")
    print("="*50)
    
    # Try to locate the internal master/history files if present
    master_key = next((k for k in dfs if 'master' in k.lower()), None)
    nav_key = next((k for k in dfs if 'nav' in k.lower() or 'history' in k.lower()), None)
    
    if not master_key or not nav_key:
        print("ℹ️ Note: Validation skipped. Local 'fund_master' or 'nav_history' CSVs are not in data/raw yet.")
        print("Once you place them there, this validation will check foreign-key mapping integrity.")
        return

    master_df = dfs[master_key]
    nav_df = dfs[nav_key]
    
    try:
        # Match code column dynamically
        m_code_col = [c for c in master_df.columns if 'code' in c.lower() or 'amfi' in c.lower()][0]
        n_code_col = [c for c in nav_df.columns if 'code' in c.lower() or 'amfi' in c.lower()][0]

        master_codes = set(master_df[m_code_col].dropna().unique())
        nav_codes = set(nav_df[n_code_col].dropna().unique())
        
        missing_in_nav = master_codes - nav_codes
        
        print(f"• Unique codes in Fund Master: {len(master_codes)}")
        print(f"• Unique codes in NAV History: {len(nav_codes)}")
        
        if len(missing_in_nav) == 0:
            print("✅ Success: Every master scheme code maps successfully to historical records.")
        else:
            print(f"⚠️ Integrity Gap: {len(missing_in_nav)} master codes do not exist in historical logs.")
    except Exception as e:
        print(f"❌ Structural layout validation failed: {e}")

if __name__ == "__main__":
    datasets = inspect_datasets()
    validate_amfi_codes(datasets)