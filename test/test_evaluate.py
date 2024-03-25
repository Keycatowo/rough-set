#%%
from roughset.evaluate import calculate_rules_ratio, evaluate_metrics
import pandas as pd
from numpy.testing import assert_allclose

def test_calculate_rules_ratio_example1():
    
    df = pd.read_csv('example.csv')

    
    # 單一條件
    assert_allclose(calculate_rules_ratio({
        "天氣": 0
        },
        df
    ), 0.4)
    assert_allclose(calculate_rules_ratio({
        "天氣": 0,
        "事故情形": None
        },
        df
    ), 0.4)
    assert_allclose(calculate_rules_ratio({
        "天氣": 0,
        "事故情形": None,
        "事故原因": None
        },
        df
    ), 0.4)
    assert_allclose(calculate_rules_ratio({
        "天氣": 0,
        "事故情形": None,
        "事故原因": None,
        "損壞部位": None
        },
        df
    ), 0.4)
    
    assert_allclose(calculate_rules_ratio({
        "天氣": 1
        },
        df
    ), 0.6)
    assert_allclose(calculate_rules_ratio({
        "事故情形": 0
        },
        df
    ), 0.2)
    assert_allclose(calculate_rules_ratio({
        "事故情形": 1
        },
        df
    ), 0.6)
    assert_allclose(calculate_rules_ratio({
        "事故情形": 2
        },
        df
    ), 0.2)
    assert_allclose(calculate_rules_ratio({
        "事故原因": 0
        },
        df
    ), 0.4)
    assert_allclose(calculate_rules_ratio({
        "事故原因": 1
        },
        df
    ), 0.6)
    assert_allclose(calculate_rules_ratio({
        "損壞部位": 0
        },
        df
    ), 0.4)
    assert_allclose(calculate_rules_ratio({
        "損壞部位": 1
        },
        df
    ), 0.6)
    
    # 多條件
    assert_allclose(calculate_rules_ratio(
        {
            "天氣": 0,
            "事故情形": 0
        },
        df
    ), 0)
    assert_allclose(calculate_rules_ratio(
        {
            "天氣": 0,
            "事故情形": 1
        },
        df
    ), 0.4)
    assert_allclose(calculate_rules_ratio(
        {
            "天氣": 1,
            "事故情形": 0
        },
        df
    ), 0.2)
    assert_allclose(calculate_rules_ratio(
        {
            "天氣": 1,
            "事故情形": 1
        },
        df
    ), 0.2)
    assert_allclose(calculate_rules_ratio(
        {
            "天氣": 1,
            "事故情形": 2
        },
        df
    ), 0.2)
    assert_allclose(calculate_rules_ratio(
        {
            "事故情形": 0,
            "事故原因": 0
        },
        df
    ), 0.2)
    
    
def test_evaluate_metrics_example1():
    
    df = pd.read_csv('example.csv')
    name_col="No"
    feature_col=['天氣', '事故情形', '事故原因']
    decision_col='損壞部位'
    
    metrics = evaluate_metrics(
        {
            "天氣": None,
            "事故情形": 0,
            "事故原因": None,
            "損壞部位": 0
        },
        df_data=df,
        name_col=name_col,
        feature_col=feature_col,
        decision_col=decision_col   
    )
    assert_allclose(metrics["support"], 0.2)
    assert_allclose(metrics["confidence"], 1.0)
    assert_allclose(metrics["lift"], 2.5)
    metrics = evaluate_metrics(
        {
            "天氣": 1,
            "事故情形": 0,
            "事故原因": None,
            "損壞部位": 0
        },
        df_data=df,
        name_col=name_col,
        feature_col=feature_col,
        decision_col=decision_col   
    )
    assert_allclose(metrics["support"], 0.2)
    assert_allclose(metrics["confidence"], 1.0)
    assert_allclose(metrics["lift"], 2.5)

    metrics = evaluate_metrics(
        {
            "天氣": None,
            "事故情形": 0,
            "事故原因": 0,
            "損壞部位": 0
        },
        df_data=df,
        name_col=name_col,
        feature_col=feature_col,
        decision_col=decision_col   
    )
    assert_allclose(metrics["support"], 0.2)
    assert_allclose(metrics["confidence"], 1.0)
    assert_allclose(metrics["lift"], 2.5)

    metrics = evaluate_metrics(
        {
            "天氣": None,
            "事故情形": 1,
            "事故原因": 0,
            "損壞部位": 1
        },
        df_data=df,
        name_col=name_col,
        feature_col=feature_col,
        decision_col=decision_col   
    )
    assert_allclose(metrics["support"], 0.2)
    assert_allclose(metrics["confidence"], 1.0)
    assert_allclose(metrics["lift"], 5/3)