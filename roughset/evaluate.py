import pandas as pd

def calculate_rules_ratio(target_dict: dict, dada_df, name_col=None) -> float:
    """
        計算 給定的規則條件 佔 所有資料 的比例
        
        Parameters:
            target_dict: dict, 規則條件, 
                key為欄位名稱, 
                value為欄位值, None代表不限制
            df: pandas.DataFrame, 資料
    """
    tmp_df = dada_df
    for col in target_dict.keys():
        if col == name_col:
            continue
        
        if target_dict[col] == None:
            continue
        tmp_df = tmp_df[tmp_df[col] ==target_dict[col]] # 逐次篩選出符合條件的資料
    return len(tmp_df) / len(dada_df)