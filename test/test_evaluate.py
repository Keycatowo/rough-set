#%%
from roughset.evaluate import calculate_rules_ratio
import pandas as pd

def test_calculate_rules_ratio_example1():
    
    df = pd.read_csv('example.csv')

    
    # 單一條件
    assert calculate_rules_ratio({
        "天氣": 0
        },
        df
    ) == 0.4
    assert calculate_rules_ratio({
        "天氣": 0,
        "事故情形": None
        },
        df
    ) == 0.4
    assert calculate_rules_ratio({
        "天氣": 0,
        "事故情形": None,
        "事故原因": None
        },
        df
    ) == 0.4
    assert calculate_rules_ratio({
        "天氣": 0,
        "事故情形": None,
        "事故原因": None,
        "損壞部位": None
        },
        df
    ) == 0.4
    
    assert calculate_rules_ratio({
        "天氣": 1
        },
        df
    ) == 0.6
    assert calculate_rules_ratio({
        "事故情形": 0
        },
        df
    ) == 0.2
    assert calculate_rules_ratio({
        "事故情形": 1
        },
        df
    ) == 0.6
    assert calculate_rules_ratio({
        "事故情形": 2
        },
        df
    ) == 0.2
    assert calculate_rules_ratio({
        "事故原因": 0
        },
        df
    ) == 0.4
    assert calculate_rules_ratio({
        "事故原因": 1
        },
        df
    ) == 0.6
    assert calculate_rules_ratio({
        "損壞部位": 0
        },
        df
    ) == 0.4
    assert calculate_rules_ratio({
        "損壞部位": 1
        },
        df
    ) == 0.6
    
    # 多條件
    assert calculate_rules_ratio(
        {
            "天氣": 0,
            "事故情形": 0
        },
        df
    ) == 0
    assert calculate_rules_ratio(
        {
            "天氣": 0,
            "事故情形": 1
        },
        df
    ) == 0.4
    assert calculate_rules_ratio(
        {
            "天氣": 1,
            "事故情形": 0
        },
        df
    ) == 0.2
    assert calculate_rules_ratio(
        {
            "天氣": 1,
            "事故情形": 1
        },
        df
    ) == 0.2
    assert calculate_rules_ratio(
        {
            "天氣": 1,
            "事故情形": 2
        },
        df
    ) == 0.2
    assert calculate_rules_ratio(
        {
            "事故情形": 0,
            "事故原因": 0
        },
        df
    ) == 0.2
    