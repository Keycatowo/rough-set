#%%
from roughset.reduct import create_reduct_rules
import pandas as pd

def test_reduct_with_none():
    
    df = pd.read_csv('example.csv')
    
    reducts = create_reduct_rules(
        df=df,
        name_col="No",
        feature_col=['天氣', '事故情形', '事故原因'],
        decision_col='損壞部位',
        include_empty=True # 包含空的reduct
    )
    
    expect_reducts = pd.read_pickle("expect/example_reducts_with_none.pkl")
    
    pd.testing.assert_frame_equal(reducts, expect_reducts)
    
def test_reduct_without_none():
    
    df = pd.read_csv('example.csv')
    
    reducts = create_reduct_rules(
        df=df,
        name_col="No",
        feature_col=['天氣', '事故情形', '事故原因'],
        decision_col='損壞部位',
        include_empty=False # 不包含空的reduct row
    )
    
    expect_reducts = pd.read_pickle("expect/example_reducts_without_none.pkl")
    
    pd.testing.assert_frame_equal(reducts, expect_reducts)
    