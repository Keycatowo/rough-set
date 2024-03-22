import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split

@st.cache_data
def convert_df(df):
    """
        Convert a pandas dataframe into a csv file.
        For the download button in streamlit.
    """
    return df.to_csv(index=False).encode('utf-8-sig')

file = st.file_uploader("Data for split", type="csv")

if file:
    file_name = file.name
    print(file_name)
    
    df = pd.read_csv(file)
    st.write("#### Original data:")
    st.dataframe(df, use_container_width=True)
    col1, col2, col3 = st.columns(3)

    # add a slider for test size
    test_size = col1.slider("Test size", 0.0, 1.0, 0.2, 0.01, help="The proportion of the dataset to include in the test split.\n Default is 0.2")

    # add a random state
    random_state = col2.number_input("Random state", value=42, help="Controls the shuffling applied to the data before applying the split.\n Default is 42.\n For the same random state, the same split will be generated. If the random state is 0, the split will be different each time.")

    # add a toggle for stratify
    stratify = col3.toggle("Stratify", help="If True, the data is split in a stratified fashion, using the target as the class labels.")
    if stratify:
        target_col = col3.selectbox("Target column", list(df.columns), help="Select the column that contains the target values.", index=len(df.columns)-1)
        
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state, stratify=df[target_col] if stratify else None)
    
    col4, col5 = st.columns(2)
    col4.write("#### Train data:")
    col4.dataframe(train_df, use_container_width=True)
    col4.download_button("Download train data", convert_df(train_df), file_name=file_name.replace(".csv", "_train.csv"), mime="text/csv")
    
    col5.write("#### Test data:")
    col5.dataframe(test_df, use_container_width=True)
    col5.download_button("Download test data", convert_df(test_df), file_name=file_name.replace(".csv", "_test.csv"), mime="text/csv")