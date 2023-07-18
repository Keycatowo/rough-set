import streamlit as st
import pandas as pd

st.header("計算約略集合欄位")
st.warning("此功能目前為Beta版本")

st.subheader("Upload a CSV file")
file = st.file_uploader("Upload a CSV file", type="csv")

if file is not None:
    df = pd.read_csv(file)
    st.write(df)
    name_col = st.selectbox("物件名稱欄位", list(df.columns), index=0)
    decision_col = st.selectbox("決策欄位", list(df.columns), index=len(df.columns)-1)
    feature_cols = st.multiselect("特徵欄位", list(df.columns), default=list(df.columns[1:-1]))

    with st.expander("欄位是否獨立"):    
        show_set = st.checkbox("顯示對應集合詳細內容", value=False, key="show_detail")
        
        select_col_all = feature_cols
        grouped_all = df.groupby(select_col_all)[name_col].apply(list)
        D_all = list(grouped_all.values)
        st.write(f"屬性集合D(**{select_col_all}**):")
        if show_set:
            st.write("{" + ",".join([f"{{{','.join(x)}}}" for x in D_all]) + "}")
        
        for col_ in feature_cols:
            st.write(f"#### D - {col_}")
            
            grouped_ = df.groupby(col_)[name_col].apply(list)
            D_ = list(grouped_.values)
            if show_set:
                st.write("{" + ",".join([f"{{{','.join(x)}}}" for x in D_]) + "}")
            is_independent = D_ == D_all
            st.write("是否獨立:", is_independent) 
    
    with st.expander("計算近似空間"):
    
        unique_decision = list(df[decision_col].unique())
        X_value = st.selectbox("集合X的值", unique_decision, index=0)
        X = df.groupby(decision_col)[name_col].apply(list)[X_value]
        st.write(f"集合X={X_value}: {{{X}}}")
        select_col = st.multiselect("屬性集合D", list(df.columns), default=list(df.columns[1:-1]))
        grouped = df.groupby(select_col)[name_col].apply(list)
        D = list(grouped.values)
        
        col3, col4 = st.columns(2)
        with col3:
            st.write("集合X的下近似集合")
            lower_set = set()
            for x in X:
                if [x] in D:
                    lower_set.add(x)
            st.write(lower_set)
            st.write("數量:", len(lower_set))
        with col4:
            st.write("集合X的上近似集合")
            upper_set = set()
            for x in X:
                for d in D:
                    if x in d:
                        upper_set.update(d)
            st.write(upper_set)
            st.write("數量:", len(upper_set))
        st.write("界限集合")
        st.write(upper_set - lower_set)
        st.write("數量:", len(upper_set - lower_set))
            
            
    
    