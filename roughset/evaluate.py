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

def row2dict(row, target_cols):
    """
        將row轉換成dict, 只取target_cols
    """
    return {col: row[col] for col in target_cols}

def evaluate_metrics(target_dict, df_data, name_col, feature_col, decision_col) -> dict:
        """
            計算 target_dict 規則 在 df_data中的 support, confidence, lift        
        """ 
        
        # 分別建立X(特徵屬性), Y(決策屬性), XY(特徵+決策)的集合
        X = row2dict(target_dict, feature_col)
        Y = row2dict(target_dict, [decision_col])
        XY = row2dict(target_dict, feature_col + [decision_col])
        
        
        # 計算support, confidence, lift
        x_score = calculate_rules_ratio(X, df_data, name_col)
        y_score = calculate_rules_ratio(Y, df_data, name_col)
        xy_score = calculate_rules_ratio(XY, df_data, name_col)
        
        
        metrics = {
            "support": x_score,
            "confidence": xy_score / x_score if x_score != 0 else None,
            "lift": xy_score / (x_score * y_score) if x_score != 0 and y_score != 0 else None
        }
        return metrics