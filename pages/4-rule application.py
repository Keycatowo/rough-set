import streamlit as st
import pandas as pd
from roughset.evaluate import calculate_rules_ratio, evaluate_metrics, row2dict

@st.cache_data
def convert_df(df):
    """
        Convert a pandas dataframe into a csv file.
        For the download button in streamlit.
    """
    return df.to_csv(index=False).encode('utf-8-sig')
   
   
st.header("Rule Application")

tab1, tab2 = st.tabs(["Upload rules/data", "Evaluate rules"])

file_rule = tab1.file_uploader("Rules", type="csv")
if file_rule:
    df_rule = pd.read_csv(file_rule)
    file_name = file_rule.name
    if "Support" in df_rule.columns:
        df_rule = df_rule.drop(columns=["Support"])
    if "Confidence" in df_rule.columns:
        df_rule = df_rule.drop(columns=["Confidence"])
    if "Lift" in df_rule.columns:
        df_rule = df_rule.drop(columns=["Lift"])
    
    tab1.dataframe(df_rule, use_container_width=True)
    
    
file_data = tab1.file_uploader("Data", type="csv")
if file_data:
    df_data = pd.read_csv(file_data)
    tab1.dataframe(df_data, use_container_width=True)
    
    
if file_rule and file_data:
    with tab1:
        name_col = st.selectbox("Object Name", list(df_data.columns), index=0, help="Select the column that contains the object names.\nDefault is the first column.")
        decision_col = st.selectbox("Decision", list(df_data.columns), index=len(df_data.columns)-1, help="Select the column that contains the dicision attribute.\nDefault is the last column.")
        feature_cols = st.multiselect("Features", list(df_data.columns), default=list(df_data.columns[1:-1]), help="Select the columns that contain the features.\nDefault is all columns except the first and last columns.")
    
    with tab2:
        
        rules_with_metrics = df_rule.copy()
        # 將 nan 填入 None
        rules_with_metrics = rules_with_metrics.where(pd.notnull(rules_with_metrics), None)
        
        
        rules_with_metrics["__rules_dict"] = rules_with_metrics.apply(lambda x: row2dict(x, feature_cols + [decision_col]), axis=1)
        rules_with_metrics["__metrics"] = rules_with_metrics["__rules_dict"].apply(lambda x: evaluate_metrics(x, df_data, name_col, feature_cols, decision_col))
        rules_with_metrics["Support"] = rules_with_metrics["__metrics"].apply(lambda x: x["support"])
        rules_with_metrics["Confidence"] = rules_with_metrics["__metrics"].apply(lambda x: x["confidence"])
        rules_with_metrics["Lift"] = rules_with_metrics["__metrics"].apply(lambda x: x["lift"])
        
        st.write(f"#### Rules with Metrics(All `{len(rules_with_metrics)}` rules)")
        st.dataframe(rules_with_metrics[feature_cols + [decision_col, "Support", "Confidence", "Lift"]], use_container_width=True)
        st.download_button("Download rules with metrics", convert_df(rules_with_metrics), file_name=file_name.replace("rules.csv", ".csv").replace(".csv", "_rules_with_test_metrics.csv"), mime="text/csv", use_container_width=True)


        st.write("#### Set Threshold")
        col1, col2, col3 = st.columns(3)
        support_th = col1.number_input("Support Threshold", min_value=0.0, max_value=1.0, value=0.0, help=f"Support Threshold is the minimum support value of the rule. In this case, the minimum support value is `{1/len(df_data):.4f}`, which means the rule must cover at least one object.")
        confidence_th = col2.number_input("Confidence Threshold", min_value=0.0, max_value=1.0, value=0.0, help="Confidence Threshold is the minimum confidence value of the rule. ")
        lift_th = col3.number_input("Lift Threshold", min_value=0.0, value=0.0, help="Lift Threshold is the minimum lift value of the rule. The default value is 0.0.")
        
        rules_filtered = rules_with_metrics[
            (rules_with_metrics["Support"] >= support_th) &
            (rules_with_metrics["Confidence"] >= confidence_th) &
            (rules_with_metrics["Lift"] >= lift_th)
        ].copy()
        st.write(f"#### Rules with Metrics (Filtered `{len(rules_filtered)}` rules)")
        st.dataframe(rules_filtered[feature_cols + [decision_col, "Support", "Confidence", "Lift"]], use_container_width=True)
        st.download_button("Download filtered rules with metrics", convert_df(rules_filtered), file_name=file_name.replace("rules.csv", ".csv").replace(".csv", "_rules_with_test_metrics_filtered.csv"), mime="text/csv", use_container_width=True)

else:
    tab2.warning("Please upload both rules and data files.")