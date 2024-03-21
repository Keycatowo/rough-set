from .reduct import create_reduct_rules
import warnings
import pandas as pd

class RoughSet:
    def __init__(self, 
                 data: pd.DataFrame, 
                 name_col: str = None, 
                 feature_col: list[str] = None, 
                 decision_col: list[str] = None
                 ):
        self.df = data
        self.name_column = name_col or data.columns[0]  # Simplified if/else syntax
        self.feature_col = feature_col or list(data.columns[1:-1])
        self.decision_col = decision_col or data.columns[-1]
        self.check_roughset_prerequisites()
        
    def check_roughset_prerequisites(self):
        """
            檢查物件是否符合RoughSet的前提
                1. 物件名稱欄位存在
                2. 物件名稱欄位不重複
                3. 特徵欄位存在
                4. 決策屬性欄位存在
            如果不符合，則拋出異常
            
            return: None
        """
        columns = self.df.columns
        name_col = self.name_column
        feature_col = self.feature_col
        decision_col = self.decision_col
        
        assert name_col in columns, f'物件名稱欄位不存在：{name_col} not in {columns}'
        assert len(self.df[name_col].unique()) == len(self.df[name_col]), f'物件欄位名稱重複：{name_col} has duplicate values'
        assert all([col in columns for col in feature_col]), f'{feature_col} not in {columns}'
        assert decision_col in columns, f'決策屬性欄位不存在：{decision_col} not in {columns}'

    
    def __getitem__(self, index):
        # 將列中的目標物件以字典形式擷取出來，如果條件不符，則拋出異常
        row = self.df.loc[self.df[self.name_column] == index].squeeze().to_dict()
        if not row:
            raise KeyError(f'物件不存在：{index} not in {self.df[self.name_column]}')

        # 將目標物件轉換成較易讀取的格式
        text = f"物件：{row[self.name_column]}\n{'-'*20}\n"
        for col in self.feature_col:
            text += f"{col}: {row[col]}\n"
        text += f"{'-'*20}\n決策屬性：{row[self.decision_col]}\n"
        print(text)
        
        return row

    def create_reduct_rules(self, include_empty=False) -> pd.DataFrame:
        """
            呼叫 reduct.create_reduct_rules 產生規則
            
            Parameters:
                include_empty: bool, default False
                    是否包含空規則
                    - True: 包含空規則
                    - False: 不包含空規則
                    
            Returns:
                reduct_rules: pandas.DataFrame, 規則
                
        """
        self.reduct_rules = create_reduct_rules(
            df=self.df,
            name_col=self.name_column,
            feature_col=self.feature_col,
            decision_col=self.decision_col,
            include_empty=include_empty
        )
        return self.reduct_rules
    
    
    def evaluate_metrics(self, support=True, confidence=True, lift=True) -> pd.DataFrame:
        """
            計算 support, confidence, lift
            
            Parameters:
                support: bool, default True
                    是否計算 support
                confidence: bool, default True
                    是否計算 confidence
                lift: bool, default True
                    是否計算 lift
                    
            Returns:
                reduct_rules: pandas.DataFrame, 包含 support, confidence, lift 的規則
        """ 
        # 先檢查是否有產生規則
        assert hasattr(self, 'reduct_rules'), '請先產生規則'
        # 分別建立X(特徵屬性), Y(決策屬性), XY(特徵+決策)的集合
        X = self.reduct_rules.apply(lambda row: self.row2dict(row, method="X"), axis=1)
        Y = self.reduct_rules.apply(lambda row: self.row2dict(row, method="Y"), axis=1)
        XY = self.reduct_rules.apply(lambda row: self.row2dict(row, method="XY"), axis=1)
        
        # 計算support, confidence, lift
        x_score = X.apply(lambda x: self.calculate_precent(x))
        y_score = Y.apply(lambda y: self.calculate_precent(y))
        xy_score = XY.apply(lambda xy: self.calculate_precent(xy))
        
        # 先檢查support, confidence, lift不在df的columns中，若存在則發起Warning
        if support and "support" in self.reduct_rules.columns:
            warnings.warn("support already in df's columns", UserWarning)
        if confidence and "confidence" in self.reduct_rules.columns:
            warnings.warn("confidence already in df's columns", UserWarning)
        if lift and "lift" in self.reduct_rules.columns:
            warnings.warn("lift already in df's columns", UserWarning)
        
        # 將結果合併到規則中
        if support:
            self.reduct_rules["support"] = x_score
        if confidence:
            self.reduct_rules["confidence"] = xy_score / x_score
        if lift:
            self.reduct_rules["lift"] = xy_score / x_score / y_score
            
        return self.reduct_rules
        
        
    
    def calculate_precent(self, target_dict: dict) -> float:
        """
            計算給定的規則條件佔所有資料的比例
        """
        tmp_df = self.df
        for col in target_dict.keys():
            if target_dict[col] == None:
                continue
            tmp_df = tmp_df[tmp_df[col] ==target_dict[col]]
        return len(tmp_df) / len(self.df)

    def row2dict(self, row: pd.Series, method="X") -> dict:
        """
        將 row 依照設定方法轉換成字典

        Parameters:
            row: A row from the dataset represented as a dictionary.
            method (str, ): The method to determine which columns to include in the dictionary.
                - 'X': Selects only the features.
                - 'Y': Selects only the decision attribute.
                - 'XY': Selects both features and the decision attribute.
        
        Returns:
            dict: A dictionary containing selected columns based on the specified method.

        Raises:
            ValueError: If the method is not one of 'X', 'Y', or 'XY'.
        """
        row_dict = dict(row)
        if method == "X":
            return {k:v for k,v in row_dict.items() if k in self.feature_col}
        elif method == "Y":
            return {k:v for k,v in row_dict.items() if k in [self.decision_col]}
        elif method == "XY":
            return {k:v for k,v in row_dict.items() if k in self.feature_col + [self.decision_col]}
        else:
            raise ValueError("method must be X, Y or XY")
        

    def positive_region(self, condition):
        # calculate positive region of a condition
        pass
    
    def negative_region(self, condition):
        # calculate negative region of a condition
        pass
    
    def boundary_region(self, condition):
        # calculate boundary region of a condition
        pass
        
    def reduct(self, attributes):
        # calculate the reduct of a set of attributes
        pass
        
    def core(self, attributes):
        # calculate the core of a set of attributes
        pass
    
    def __repr__(self) -> str:
        repr_ = "RoughSet\n\n"
        
        repr_ += f"\tName column: {self.name_column}\n"
        repr_ += f"\tFeature columns: {self.feature_col}\n"
        repr_ += f"\tDecision column: {self.decision_col}\n\n"
        
        repr_ += f"\tNumber of objects: {len(self.df)}\n"
        repr_ += f"\tNumber of unique decision values: {len(self.df[self.decision_col].unique())}\n"
        
        if hasattr(self, 'reduct_rules'):
            repr_ += f"\tNumber of reduct rules: {len(self.reduct_rules)}\n"
        else:
            repr_ += "\tNo reduct rules now, use create_reduct_rules to generate reduct rules\n"
            
        return repr_