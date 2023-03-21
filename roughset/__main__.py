from .reduct import create_reduct_rules
import warnings

class RoughSet:
    def __init__(self, data, name_col=None, feature_col=None, decision_col=None):
        """
        """
        # 
        self.df = data
        if name_col is None:
            self.name_column = data.columns[0]
        else:
            self.name_column = name_col
        if feature_col is None:
            self.feature_col = list(data.columns[1:-1])
        else:
            self.feature_col = feature_col
        if decision_col is None:
            self.decision_col = data.columns[-1]
        else:
            self.decision_col = decision_col
        self.check_roughset_prerequisites()
        
    def check_roughset_prerequisites(self):
        columns = self.df.columns
        name_col = self.name_column
        feature_col = self.feature_col
        decision_col = self.decision_col
        
        # name_col 存在於 columns
        assert name_col in columns, f'物件名稱欄位不存在：{name_col} not in {columns}, '
        # 所有name_col的值都不重複
        assert len(self.df[name_col].unique()) == len(self.df[name_col]), f'決策欄位名稱重複：{name_col} has duplicate values'
        # feature_col 存在於 columns
        assert all([col in columns for col in feature_col]), f'{feature_col} not in {columns}'
        # decision_col 存在於 columns
        assert decision_col in columns, f'決策屬性欄位不存在：{decision_col} not in {columns}'
    
    def __getitem__(self, index):
        row = self.df[self.df[self.name_column] == index]
        assert len(row) == 1, f'物件不存在：{index} not in {self.df[self.name_column]}'
        text = ""
        text += f"物件：{row[self.name_column]}\n"
        text += "-"*20 + "\n"
        for col in self.feature_col:
            text += f"{col}: {row[col]}\n"
        text += "-"*20 + "\n"
        text += f"決策屬性：{row[self.decision_col]}\n"
        print(text)
        
        return row

    def create_reduct_rules(self, include_empty=False):
        """
            呼叫 reduct.create_reduct_rules 產生規則
        """
        self.reduct_rules = create_reduct_rules(
            df=self.df,
            name_col=self.name_column,
            feature_col=self.feature_col,
            decision_col=self.decision_col,
            include_empty=include_empty
        )
        return self.reduct_rules
    
    
    def evaluate_metrics(self, support=True, confidence=True, lift=True):
        """
            計算support, confidence, lift。
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
        
        
    
    def calculate_precent(self, target_dict):
        """
        計算給定的規則條件佔所有資料的比例
        """
        tmp_df = self.df
        for col in target_dict.keys():
            if target_dict[col] == None:
                continue
            tmp_df = tmp_df[tmp_df[col] ==target_dict[col]]
        return len(tmp_df) / len(self.df)

    def row2dict(self, row, method="X"):
        """
            X: 所有的特徵的集合
            Y: 決策屬性的集合
            XY: 特徵+決策屬性的集合
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