import streamlit as st
import pandas as pd
from roughset.relations import get_equivalence_object, is_set_same, get_lower_approximation, get_upper_approximation

def display_euqivalence_set(df, name_col, target_cols, title):
    with st.expander(title):
        eq = get_equivalence_object(df, name_col, target_cols)
        st.write("Condition attributes: `{" + ", ".join([str(x) for x in target_cols]) + "}`")
        value_text_list = []
        for k, v in eq.items():
            value_text = "{" + ", ".join([str(x) for x in v]) + "}"
            st.write(f"+ **{k}**: `{value_text}`")
            value_text_list.append(value_text)
        st.write("Equivalence set:")
        st.code("{" + ", ".join(value_text_list) + "}")
        return eq

st.header("Feature Independence Check")

tab1, tab2, tab3 = st.tabs(["Upload data", "Check independence", "Approximation"])

st.session_state["file"] = tab1.file_uploader("Data", type="csv")
if st.session_state["file"] is not None:
    with tab1: 
        
        df = pd.read_csv(st.session_state["file"])
        st.dataframe(df, use_container_width=True)
        name_col = st.selectbox("Object Name", list(df.columns), index=0, help="Select the column that contains the object names.\nDefault is the first column.")
        decision_col = st.selectbox("Decision", list(df.columns), index=len(df.columns)-1, help="Select the column that contains the dicision attribute.\nDefault is the last column.")
        feature_cols = st.multiselect("Features", list(df.columns), default=list(df.columns[1:-1]), help="Select the columns that contain the features.\nDefault is all columns except the first and last columns.")

    

    with tab2:
        st.caption("Explain of independent:<br>For a feature `f` in all features `F`, if $U|(F-f) = U$, then `f` is **dependent** on other features, otherwise `f` is **independent**.", unsafe_allow_html=True)
        
        st.write("**U**: `{"+ ", ".join([str(x) for x in df[name_col].to_list()]) + "}`")
        st.write("**F**: `{"+ ", ".join([str(x) for x in feature_cols]) + "}`")
        
        target_cols = feature_cols + [decision_col]
        eq_all_decision = display_euqivalence_set(df, name_col, target_cols, "##### Equivalence relations with all features and decision")
        st.write("---")
        
        
        target_cols = feature_cols
        eq_all = display_euqivalence_set(df, name_col, target_cols, "##### Equivalence relations with all features")
        
        for col in feature_cols:
            st.write("---")
            target_cols = [c for c in feature_cols if c != col]
            eq_col = display_euqivalence_set(df, name_col, target_cols, f"##### Equivalence relations without `{col}`")
            
            if is_set_same(list(eq_all.values()), list(eq_col.values())):
                st.write(f"`{col}` is a **dependent** feature.")
            else:
                st.write(f"`{col}` is a **independent** feature.")
        
    with tab3:
        unique_decision = list(df[decision_col].unique())
        X_value = st.selectbox(f"Select decision value for $X$: `{decision_col}`=", unique_decision, index=0)
        X = df.groupby(decision_col)[name_col].apply(list)[X_value]
        X = sorted(list(X))
        X_text = "{" + ", ".join([str(x) for x in X]) + "}"
        st.write("Objects in $X$:")
        st.code(X_text)
        # st.write("**U**: `{"+ ", ".join([str(x) for x in df[name_col].to_list()]) + "}`")
        st.write("**F**: `{"+ ", ".join([str(x) for x in feature_cols]) + "}`")
        st.write("---")

        lower_set = get_lower_approximation(df, name_col, feature_cols, decision_col, X_value) 
        lower_set = set(sorted(list(lower_set)))
        print("Lower set:", lower_set)
        with st.expander(f"**Lower approximation set** \t(`{len(lower_set)}` objects)", expanded=True):
            st.code("{" + ", ".join([str(x) for x in lower_set]) + "}")
        
        upper_set = get_upper_approximation(df, name_col, feature_cols, decision_col, X_value)
        upper_set = set(sorted(list(upper_set)))
        print("Upper set:", upper_set)
        with st.expander(f"**Upper approximation set** \t(`{len(upper_set)}` objects)", expanded=True):
            st.code("{" + ", ".join([str(x) for x in upper_set]) + "}")
        
        boundary_set = upper_set - lower_set
        boundary_set = set(sorted(list(boundary_set)))
        print("Boundary set:", boundary_set)
        with st.expander(f"**Boundary set** \t(`{len(boundary_set)}` objects)", expanded=True):
            st.code("{" + ", ".join([str(x) for x in boundary_set]) + "}")
else:
    tab2.warning("Please upload a CSV file first.")
    tab3.warning("Please upload a CSV file first.")
        