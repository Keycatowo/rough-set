import pandas as pd

def get_equivalence_object(df:pd.DataFrame, name_col: str, target_cols: list[str]) -> dict:
    """
        取得 target_cols 相等的物件，相同的物件會被放在同一個set中
        
        Parameters
        ----------
        df: pandas.DataFrame
        name_col: str, 物件名稱欄位
        target_cols: list[str], 目標欄位列表
        
        return: dict, key是target_cols相等的值, values是df中name_col欄位的值
        
        範例：
        
        df:
           No  天氣  事故情形  事故原因  損壞部位
            0   1   0     1     1     0
            1   2   1     0     0     0
            2   3   1     2     1     1
            3   4   0     1     1     1
            4   5   1     1     0     1
        
        get_equivalence_object(df, name_col, ["天氣"]) # {0: {1, 4}, 1: {2, 3, 5}}
        get_equivalence_object(df, name_col, ["事故原因", "損壞部位"])  # {(0, 0): {2}, (0, 1): {5}, (1, 0): {1}, (1, 1): {3, 4}}
        
    """
    
    # 檢查df是否符合要求
    assert name_col in df.columns, f"{name_col} not in {df.columns}"
    for col in target_cols:
        assert col in df.columns, f"{col} not in {df.columns}"  
        
    # 取得相等的物件
    grouped = df.groupby(target_cols)[name_col].apply(list)
    
    # 依次加入 dict
    equivalence_dict = {}
    for key, value in grouped.items():
        equivalence_dict[key] = set(value)
    
    return equivalence_dict