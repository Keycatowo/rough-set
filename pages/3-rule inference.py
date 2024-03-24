import pandas as pd
import streamlit as st
from roughset import RoughSet
from roughset.evaluate import calculate_rules_ratio, evaluate_metrics, row2dict


def rule_explain(rule: dict, name_col: str, feature_col: list[str], decision_col: str):
    rule_text = "**IF** \n\n"
    # add text for feature
    for col, value in rule.items():
        if value is None:
            continue
        
        if col in feature_col:
            rule_text += f"+ {col} = `{value}` \n\n"
            
    # add text for decision
    rule_text += f"**THEN** \n\n+ {decision_col} = `{rule[decision_col]}`\n\n"
    
    # add text for object name
    rule_text += f"> This rule is reduct from object Name: `{rule[name_col]}`"
    
    st.markdown(rule_text)
    return rule_text

@st.cache_data
def convert_df(df):
    """
        Convert a pandas dataframe into a csv file.
        For the download button in streamlit.
    """
    return df.to_csv(index=False).encode('utf-8-sig')
   

st.header("Rule Inference")

tab1, tab2, tab3 = st.tabs(["Upload data", "Reduct rules", "Select rules"])

st.session_state["file"] = tab1.file_uploader("Data", type="csv")
if st.session_state["file"] is not None:
    with tab1: 
        
        df = pd.read_csv(st.session_state["file"])
        file_name = st.session_state["file"].name
        st.dataframe(df, use_container_width=True)
        name_col = st.selectbox("Object Name", list(df.columns), index=0, help="Select the column that contains the object names.\nDefault is the first column.")
        decision_col = st.selectbox("Decision", list(df.columns), index=len(df.columns)-1, help="Select the column that contains the dicision attribute.\nDefault is the last column.")
        feature_cols = st.multiselect("Features", list(df.columns), default=list(df.columns[1:-1]), help="Select the columns that contain the features.\nDefault is all columns except the first and last columns.")

   
    with tab2:
        rule_info_container = st.container()
        
        RS = RoughSet(df, name_col, feature_cols, decision_col)
        rules = RS.create_reduct_rules()
        rules_without_name = rules[feature_cols + [decision_col]]
        rules_without_name_dedup = rules_without_name.drop_duplicates() # drop duplicate rows
        
        st.write("#### Reduct Rules")
        st.dataframe(rules, use_container_width=True)
        
        # add a index selection
        st.write("#### Rule Explain")
        selected_index = st.slider("Select the index of rule", 0, len(rules)-1, 0)
        selected_rules_row = rules.iloc[selected_index]
        # st.dataframe(selected_rules_row, use_container_width=True)
        print(selected_rules_row.to_dict())
        
        rule_explain(rule=selected_rules_row.to_dict(), name_col=name_col, feature_col=feature_cols, decision_col=decision_col)
        
        rule_info_container.write("#### Rule Information")
        rule_info_container.write(f"**Number of rules**: `{len(rules)}`")
        rule_info_container.write(f"**Number of rules(deduplication)**: `{len(rules_without_name_dedup)}`" )
        
        
        
    with tab3:
        

        
        rules_with_metrics = rules_without_name_dedup.copy()

        rules_with_metrics["__rules_dict"] = rules_with_metrics.apply(lambda x: row2dict(x, feature_cols + [decision_col]), axis=1)
        rules_with_metrics["__metrics"] = rules_with_metrics["__rules_dict"].apply(lambda x: evaluate_metrics(x, df, name_col, feature_cols, decision_col))
        rules_with_metrics["Support"] = rules_with_metrics["__metrics"].apply(lambda x: x["support"])
        rules_with_metrics["Confidence"] = rules_with_metrics["__metrics"].apply(lambda x: x["confidence"])
        rules_with_metrics["Lift"] = rules_with_metrics["__metrics"].apply(lambda x: x["lift"])
        
        st.write(f"#### Rules with Metrics(All `{len(rules_with_metrics)}` rules)")
        st.dataframe(rules_with_metrics[feature_cols + [decision_col, "Support", "Confidence", "Lift"]], use_container_width=True)
        
        st.write("#### Set Threshold")
        col1, col2, col3 = st.columns(3)
        support_th = col1.number_input("Support Threshold", min_value=0.0, max_value=1.0, value=0.0, help=f"Support Threshold is the minimum support value of the rule. In this case, the minimum support value is `{1/len(df):.4f}`, which means the rule must cover at least one object.")
        confidence_th = col2.number_input("Confidence Threshold", min_value=0.0, max_value=1.0, value=0.0, help="Confidence Threshold is the minimum confidence value of the rule. Since the rule is reduct from the decision, all rules have a confidence of 1.0.")
        lift_th = col3.number_input("Lift Threshold", min_value=0.0, value=0.0, help="Lift Threshold is the minimum lift value of the rule. The default value is 0.0.")
        
        rules_filtered = rules_with_metrics[
            (rules_with_metrics["Support"] >= support_th) &
            (rules_with_metrics["Confidence"] >= confidence_th) &
            (rules_with_metrics["Lift"] >= lift_th)
        ].copy()
        st.write(f"#### Rules with Metrics (Filtered `{len(rules_filtered)}` rules)")
        st.dataframe(rules_filtered[feature_cols + [decision_col, "Support", "Confidence", "Lift"]], use_container_width=True)
        
        
        st.download_button("Download rules with metrics", convert_df(rules_filtered), file_name=file_name.replace(".csv", "_rules_with_metrics.csv"), mime="text/csv", use_container_width=True)
        st.download_button("Download rules without metrics", convert_df(rules_filtered[feature_cols + [decision_col]]), file_name=file_name.replace(".csv", "_rules.csv"), mime="text/csv", use_container_width=True)

        
else:
    tab2.warning("Please upload a CSV file first.")
    tab3.warning("Please upload a CSV file first.")
        