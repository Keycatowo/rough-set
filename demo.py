import streamlit as st
import pandas as pd
from roughset import RoughSet

@st.cache_data
def convert_df(df):
    """
        Convert a pandas dataframe into a csv file.
        For the download button in streamlit.
    """
    return df.to_csv(index=False).encode('utf-8')


st.header("Rough Set Demo")
st.write("This is a demo of the rough set package.")

with st.expander("Upload data"):
    file = st.file_uploader("Upload a CSV file", type="csv")
    if file is not None:
        df = pd.read_csv(file)
        st.write(df)
        
        with st.form("確認欄位名稱"):
            name_col = st.selectbox("物件名稱欄位", list(df.columns), index=0)
            feature_cols = st.multiselect("特徵欄位", list(df.columns), default=list(df.columns[1:-1]))
            decision_col = st.selectbox("決策欄位", list(df.columns), index=len(df.columns)-1)
            submit = st.form_submit_button("計算約略集合規則")

if submit or st.session_state.sumbbit:
    st.session_state.sumbbit = True
    RS = RoughSet(df, name_col, feature_cols, decision_col)
    rules = RS.create_reduct_rules()
    rules_with_metrics = RS.evaluate_metrics()
    
    col1, col2, col3 = st.columns(3)
    with col1: support_th = st.number_input("Support Threshold", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    with col2: confidence_th = st.number_input("Confidence Threshold", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    with col3: lift_th = st.number_input("Lift Threshold", min_value=0.0, value=0.0, step=0.01)
    
    rules_filtered = rules_with_metrics[(rules_with_metrics["support"] >= support_th) & (rules_with_metrics["confidence"] >= confidence_th) & (rules_with_metrics["lift"] >= lift_th)]
    st.dataframe(rules_filtered)
    st.download_button("Download", convert_df(rules_filtered), file_name="rules.csv", mime="text/csv")
    