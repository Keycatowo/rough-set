"""
    使用Mohapatra資料測試計算metrics：支持度、信賴度、增益
"""
from roughset import RoughSet
import pandas as pd

def test_metrics():
    
    df = pd.read_csv("Mohapatra.csv")
    
    RS = RoughSet(
        data=df,
        name_col="Company",
        feature_col=['Mkt(a1)', 'Advt(a2)', 'Dist(a3)', 'Misc(a4)', 'R&D(a5)'],
        decision_col='Sales(D)',
    )
    
    rules = RS.create_reduct_rules(include_empty=False)
    rules_with_score = RS.evaluate_metrics()
    
    assert rules_with_score.shape[0] == 393 # 初始有393個rules
    
    rules_with_score = rules_with_score.drop(columns=['Company'])
    rules_with_score = rules_with_score.drop_duplicates()
    
    assert rules_with_score.shape[0] == 70 # 去除重複的rules後剩下70個
    
    rules_with_score = rules_with_score[rules_with_score['support'] > 0.25]
    
    assert rules_with_score.shape[0] == 20 # 篩選support > 0.25 的rules後剩下20個
    
    expect_rules_with_score = pd.read_pickle("expect/Mohapatra_rules_with_score.pkl")
    
    pd.testing.assert_frame_equal(rules_with_score, expect_rules_with_score)