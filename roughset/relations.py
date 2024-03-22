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
            1   0      1          1         0
            2   1      0          0         0
            3   1      2          1         1
            4   0      1          1         1
            5   1      1          0         1
        
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


def get_lower_approximation(df, name_col: str, target_cols: list[str], decision_col: str, decision_value) -> set:
    """
    Get the lower approximation set based on the given decision value.

    Args:
        df (DataFrame): The input DataFrame.
        name_col (str): The name of the column containing the object names.
        target_cols (list[str]): The list of column names representing the target attributes.
        decision_col (str): The name of the column representing the decision attribute.
        decision_value: The value of the decision attribute to consider.

    Returns:
        set: The lower approximation set.

    Raises:
        AssertionError: If the required columns are not present in the DataFrame or if the decision value is not found in the decision column.

        範例：
        
        df:
           No  天氣  事故情形  事故原因  損壞部位
            1   0      1          1         0
            2   1      0          0         0
            3   1      2          1         1
            4   0      1          1         1
            5   1      1          0         1
            
        get_lower_approximation(df, "No", ["天氣", "事故情形"], "損壞部位", 1) # {3, 5}
    """
    # 檢查df是否符合要求
    assert name_col in df.columns, f"{name_col} not in {df.columns}"
    for col in target_cols:
        assert col in df.columns, f"{col} not in {df.columns}"  
    # decision_col 等於 decision_value 的資料筆數不為0
    assert len(df[df[decision_col] == decision_value]) != 0, f"Decision value [{decision_value}] not in {decision_col}!"
    
    D_dict = get_equivalence_object(df=df, name_col=name_col, target_cols=target_cols) # 條件欄位的等價物件
    X_all = get_equivalence_object(df=df, name_col=name_col, target_cols=[decision_col]) # 目標欄位的等價物件
    
    X = X_all[decision_value] # 取得目標欄位的等價物件
    
    lower_set = [] # 雖然命名為set,但必須要用list儲存(set內不能存放set)
    for x in X:
        for d in D_dict.values():
            if x in d and d <= X:
                lower_set.append(x)
                break
    return set(lower_set)

def get_upper_approximation(df, name_col: str, target_cols: list[str], decision_col: str, decision_value) -> set:
    """
    Get the upper approximation set based on the given decision value.

    Args:
        df (DataFrame): The input DataFrame.
        name_col (str): The name of the column containing the object names.
        target_cols (list[str]): The list of column names representing the target attributes.
        decision_col (str): The name of the column representing the decision attribute.
        decision_value: The value of the decision attribute to consider.

    Returns:
        set: The upper approximation set.

    Raises:
        AssertionError: If the required columns are not present in the DataFrame or if the decision value is not found in the decision column.

        範例：
        
        df:
           No  天氣  事故情形  事故原因  損壞部位
            1   0      1          1         0
            2   1      0          0         0
            3   1      2          1         1
            4   0      1          1         1
            5   1      1          0         1
            
        get_upper_approximation(df, "No", ["天氣", "事故情形"], "損壞部位", 1) # {1, 3, 4, 5}
    """
    
    # 檢查df是否符合要求
    assert name_col in df.columns, f"{name_col} not in {df.columns}"
    for col in target_cols:
        assert col in df.columns, f"{col} not in {df.columns}"  
    # decision_col 等於 decision_value 的資料筆數不為0
    assert len(df[df[decision_col] == decision_value]) != 0, f"Decision value [{decision_value}] not in {decision_col}!"
    
    D_dict = get_equivalence_object(df=df, name_col=name_col, target_cols=target_cols) # 條件欄位的等價物件
    X_all = get_equivalence_object(df=df, name_col=name_col, target_cols=[decision_col]) # 目標欄位的等價物件
    
    X = X_all[decision_value] # 取得目標欄位的等價物件
    
    upper_set = [] # 雖然命名為set,但必須要用list儲存(set內不能存放set)

    for x in X:
        for d in D_dict.values():
            if x in d:
                upper_set.extend(d)
                break

    return set(upper_set)

def is_set_same(set1: list[set], set2:list[set]):
    """
        檢查兩個set list是否相等
    """
    
    for s1 in set1:
        if s1 not in set2:
            return False
        
    for s2 in set2:
        if s2 not in set1:
            return False
        
    return True
    