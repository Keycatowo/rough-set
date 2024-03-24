import streamlit as st
import pandas as pd


st.header("Rough Set Demo")
st.write("This is a demo of package **roughset**.")

st.subheader("Stage 0: Prepare Data")

st.write("In this stage, you will prepare the data for the rough set analysis.")
st.write("""
####  Data requirements:
- Data should be a `.csv` file.
- Contains multiple columns
    - One of the columns should be the object name, default is the first column.
    - One of the columns should be the decision attribute, default is the last column.
    - The rest of the columns are the feature attributes.
""")
df_exmaple = pd.read_csv("example/Mohapatra/Mohapatra.csv")
st.write("#### Example Data")
st.dataframe(df_exmaple, use_container_width=True)


st.subheader("Stage 1: Select Feature")
st.write("In this stage, you can upload the data, and check if the feature is **independent** or **dependent**.")
st.write("In addition, you can also check the **upper approximation**, **lower approximation**, and **boundary region** of the decision value.")
st.page_link("pages/1-select feature.py", label="Select Feature", icon="1️⃣")


st.subheader("Stage 2: Split Data")
st.write("In this stage, you can split the data into **training** and **testing** data.")
st.page_link("pages/2-data process.py", label="Data Process", icon="2️⃣")
stage2_col1, stage2_col2 = st.columns(2)
with stage2_col1:
    st.write("#### Training Data")
    df_train = pd.read_csv("example/Mohapatra/Mohapatra_train.csv")
    st.dataframe(df_train, use_container_width=True)
with stage2_col2:
    st.write("#### Testing Data")
    df_test = pd.read_csv("example/Mohapatra/Mohapatra_test.csv")
    st.dataframe(df_test, use_container_width=True)



st.subheader("Stage 3: Rough Set Analysis")
st.write("In this stage, you can get the **reduct rules** from the training data.")
st.write("In addition, you can also set the **threshold** for reduct rules, and download the **filtered rules**.")
st.page_link("pages/3-rule inference.py", label="Rough Set Analysis", icon="3️⃣")

st.write("#### Example Rules")
df_rules = pd.read_csv("example/Mohapatra/Mohapatra_train_rules.csv")
st.dataframe(df_rules, use_container_width=True)

st.write("#### Example Rules with metrics")
df_rules_metrics = pd.read_csv("example/Mohapatra/Mohapatra_train_rules_with_metrics.csv")
df_rules_metrics.drop(columns=["__rules_dict", "__metrics"], inplace=True)
st.dataframe(df_rules_metrics, use_container_width=True)


st.subheader("Stage 4: Evaluation")
st.write("In this stage, you can evaluate the rulee with the testing data.")
st.write("You can get the **Support**, **Confidence**, **Lift** of the rules.")
st.page_link("pages/4-rule application.py", label="Evaluation", icon="4️⃣")
st.write("#### Example Evaluation")
df_eval = pd.read_csv("example/Mohapatra/Mohapatra_train__rules_with_test_metrics.csv")
df_eval.drop(columns=["__rules_dict", "__metrics"], inplace=True)
st.dataframe(df_eval, use_container_width=True)