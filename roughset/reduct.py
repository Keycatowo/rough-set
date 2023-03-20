import pandas as pd
from itertools import combinations

DEBUG = False

def check_df(df, name_col, feature_col, decision_col):
    """
    檢查df是否符合要求
    df: pandas.DataFrame
    name_col: str, 物件名稱欄位, 必須存在於df.columns 且 所有name_col的值都不重複
    feature_col: list, 特徵欄位, 必須存在於df.columns
    decision_col: str, 決策欄位, 必須存在於df.columns
    """
    columns = df.columns
    if DEBUG:
        print(
            f"name_col: {name_col}\n",
            f"feature_col: {feature_col}\n",
            f"decision_col: {decision_col}\n"
        )
    #%% 檢查
    # name_col 存在於 columns
    assert name_col in columns, f'{name_col} not in {columns}'
    # 所有name_col的值都不重複
    assert len(df[name_col].unique()) == len(df[name_col]), f'{name_col} has duplicate values'
    # feature_col 存在於 columns
    assert all([col in columns for col in feature_col]), f'{feature_col} not in {columns}'
    # decision_col 存在於 columns
    assert decision_col in columns, f'{decision_col} not in {columns}'
    
#%% 建立decision dictionary
def create_decision_dict(df, name_col, decision_col):
    """
    建立decision dictionary
    df: pandas.DataFrame
    name_col: str, 物件名稱欄位
    decision_col: str, 決策欄位
    
    return: dict, key是decision_values, values是是df中decision_col欄位為key的name_col欄位的值
        例： {0: {1, 2}, 1: {3, 4, 5}}
    """
    decision_values = df[decision_col].unique()
    # 建立一個set，key是decision_values, values是是df中decision_col欄位為key的name_col欄位的值
    decision_dict = {key: set(df[df[decision_col] == key][name_col]) for key in decision_values}
    return decision_dict

#%% 建立reduct dictionary
def create_reduct_dict_by_row(df, row, name_col, feature_col):
    """
    建立reduct dictionary
    df: pandas.DataFrame
    row: pandas.Series, 要比對的物件
    name_col: str, 物件名稱欄位
    feature_col: list, 特徵欄位
    decision_col: str, 決策欄位
    
    return: dict, key是features, values是是df中decision_col欄位為key的name_col欄位的值
        例： {(1,): {1, 2}, (1, 2): {1, 2, 3}}
    """
    reduct_dict = {}
    for num_features in range(1, len(feature_col)):
        for features in combinations(feature_col, num_features):
            df_selected = df # 取出一份df
            for feature in features:
                value = row[feature]
                df_selected = df_selected[df_selected[feature] == value] # 依序過濾
            reduct_dict[features] = set(df_selected[name_col]) # 將過濾後的df的name_col欄位的值存入reduct_dict
    return reduct_dict


#%% 過濾reduct dictionary
def filter_reduct_dict_by_row(row, name_col, decision_dict, reduct_dict):
    """
    過濾reduct dictionary
    Args:
        row: pandas.Series, 要比對的物件
        name_col: str, 物件名稱欄位
        decision_dict: dict, key是decision_values, values是是df中decision_col欄位為key的name_col欄位的值
            例：{0: {1, 2}, 1: {3, 4, 5}}
        reduct_dict: dict, key是features, values是是df中decision_col欄位為key的name_col欄位的值
            例：{('天氣',): {2, 3, 5},
                ('事故情形',): {2},
                ('事故原因',): {2, 5},
                ('天氣', '事故情形'): {2},
                ('天氣', '事故原因'): {2, 5},
                ('事故情形', '事故原因'): {2}}
    Return:
        reduct_result: list, reduct rules
            例：[('事故情形',), ('天氣', '事故情形'), ('事故情形', '事故原因')]
    """
    # 取得decision_dict中value有包含row[name_col]的value
    # 例： {1, 2}
    decision = [value for key, value in decision_dict.items() if row[name_col] in value][0]

    #%%
    # 對所有的reduct_dict的value
    # 分別去計算是否為decision的子集
    # 加入所有的decision的子集到reduct_dict_final
    reduct_result = []
    for key, value in reduct_dict.items():
        if DEBUG:
            print(key, value, value.issubset(decision))
        if value.issubset(decision):
            reduct_result.append(key)
    return reduct_result



#%% 建立reduct rules dataframe
def create_reduct_rules_by_row(df, row, columns, name_col, decision_col, reduct_result, include_empty=False):

    # 針對產生出來的結果，建立一個新的dataframe
    df_rule = pd.DataFrame(columns=columns)
    # 先建立一個empty的row
    empty_row = pd.Series([None] * len(columns), index=columns)


    for rule in reduct_result:
    
        new_row = empty_row.copy()
        for feature in rule:
            new_row[feature] = row[feature]
        new_row[name_col] = row[name_col]
        new_row[decision_col] = row[decision_col]
        
        df_rule = pd.concat([df_rule, new_row.to_frame().T], ignore_index=True)
        
    # 若df_rule是空的，則仍然加入一個row
    if df_rule.empty and include_empty:
        new_row = empty_row.copy()
        new_row[name_col] = row[name_col]
        df_rule = pd.concat([df_rule, new_row.to_frame().T], ignore_index=True)
        
    return df_rule
    


#%% 建立整個流程
def create_reduct_rules(df, name_col, feature_col, decision_col, include_empty=False):
    """
    建立整個流程
    """
    # 檢查columns
    check_df(df, name_col, feature_col, decision_col)
    columns = [name_col] + feature_col + [decision_col]
    
    # 建立決策目標的值的集合
    decision_dict = create_decision_dict(df, name_col, decision_col)
    
    df_rule = pd.DataFrame(columns=columns)
    # 依照每一個row進行處理
    for index, row in df.iterrows():
        reduct_dict = create_reduct_dict_by_row(df, row, name_col, feature_col) # 建立這個row的不同數量特徵產生的約略集合
        reduct_result = filter_reduct_dict_by_row(row, name_col, decision_dict, reduct_dict) # 過濾約略集合，只留下決策目標的子集合
        row_rules = create_reduct_rules_by_row(df, row, columns, name_col, decision_col, reduct_result, include_empty) # 建立reduct rules dataframe
        df_rule = pd.concat([df_rule, row_rules], ignore_index=True)
    return df_rule


