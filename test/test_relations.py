from roughset.relations import get_equivalence_object, get_lower_approximation, get_upper_approximation
import pandas as pd

def test_get_equivalence_object_example1():
    """
        以範例1測試 get_equivalence_object
        參考值來自於 《大數據分析與資料挖礦》 p.122
    """
    
    df = pd.read_csv('example.csv')
    
    
    assert get_equivalence_object(df, "No", ["天氣"]) == {0: {1, 4}, 1: {2, 3, 5}}
    assert get_equivalence_object(df, "No", ["事故情形"]) == {0: {2}, 1: {1, 4, 5}, 2: {3}}
    assert get_equivalence_object(df, "No", ["事故原因"]) == {0: {2, 5}, 1: {1, 3, 4}}
    assert get_equivalence_object(df, "No", ["損壞部位"]) == {1: {3, 4, 5}, 0: {1, 2}}
    assert get_equivalence_object(df, "No", ["天氣", "事故原因"])  == {(0, 1): {1, 4}, (1, 0): {2, 5}, (1, 1): {3}}
    assert get_equivalence_object(df, "No", ["天氣", "事故情形", "事故原因"]) == {(0, 1, 1): {1, 4}, (1, 0, 0): {2}, (1, 1, 0): {5}, (1, 2, 1): {3}}
    assert get_equivalence_object(df, "No", ["天氣", "事故情形"]) == {(0, 1): {1, 4}, (1, 0): {2}, (1, 1): {5}, (1, 2): {3}}
    
    
def test_get_equivalence_object_example2():
    """
        以範例2測試 get_equivalence_object
        參考值來自於 《大數據分析與資料挖礦》 p.135
    """
    
    df = pd.read_csv('Mohapatra.csv')
    
    assert get_equivalence_object(df, "Company", ["Mkt(a1)", "Dist(a3)"]) == {
        ('L', 'L'): {'C1', 'C3', 'C4', 'C5', 'C6', 'C8', 'C11', 'C12', 'C14', 'C16', 'C17', 'C18', 'C20', 'C21', 'C22', 'C23'},
        ('A', 'L'): {'C2', 'C7', 'C15', 'C19'}, 
        ('L', 'H'): {'C10'}, 
        ('H', 'L'): {'C9', 'C13'}, 
        }

    X_all = get_equivalence_object(df, "Company", ["Sales(D)"])
    
    X1 = X_all['H']
    X2 = X_all['A']
    X3 = X_all['L']
    
    assert X1 == {'C2', 'C10', 'C15'}
    assert X2 == {'C19', 'C7'}
    assert X3 == {'C1', 'C3', 'C4', 'C5', 'C6', 'C8', 'C9', 'C11', 'C12', 'C13', 'C14', 'C16', 'C17', 'C18', 'C20', 'C21', 'C22', 'C23'}


def test_get_lower_approximation_example1():
    """
        以範例1測試 get_lower_approximation
        參考值來自於 《大數據分析與資料挖礦》 p.122
    """
    
    df = pd.read_csv('example.csv')
    
    assert get_lower_approximation(df, "No", ["天氣", "事故情形"], "損壞部位", 1) == {3, 5}
    
def test_get_lower_approximation_example2():
    """
        以範例2測試 get_lower_approximation
        參考值來自於 《大數據分析與資料挖礦》 p.135
    """
    
    df = pd.read_csv('Mohapatra.csv')
    
    assert get_lower_approximation(df, "Company", ["Mkt(a1)", "Dist(a3)"], "Sales(D)", "H") == {'C10'}
    assert get_lower_approximation(df, "Company", ["Mkt(a1)", "Dist(a3)"], "Sales(D)", "A") == set()
    assert get_lower_approximation(df, "Company", ["Mkt(a1)", "Dist(a3)"], "Sales(D)", "L") == {'C1', 'C11', 'C12', 'C13', 'C14', 'C16', 'C17', 'C18', 'C20', 'C21', 'C22', 'C23', 'C3', 'C4', 'C5', 'C6', 'C8', 'C9'}

def test_get_lower_approximation_example3():
    """
        以範例3測試 get_lower_approximation
        
    """
    
    df = pd.read_csv("Blood_disease.csv")
    
    assert get_lower_approximation(df, "Sample", ["Blood type"], "Disease", 1) == set()
    
    
def test_get_upper_approximation_example1():
    """
        以範例1測試 get_upper_approximation
        參考值來自於 《大數據分析與資料挖礦》 p.122
    """
    
    df = pd.read_csv('example.csv')
    
    assert get_upper_approximation(df, "No", ["天氣", "事故情形"], "損壞部位", 1) == {1, 3, 4, 5}
    
def test_get_upper_approximation_example2():
    """
        以範例2測試 get_upper_approximation
        參考值來自於 《大數據分析與資料挖礦》 p.135
    """
    
    df = pd.read_csv('Mohapatra.csv')
    
    assert get_upper_approximation(df, "Company", ["Mkt(a1)", "Dist(a3)"], "Sales(D)", "H") == {'C10', 'C15', 'C19', 'C2', 'C7'}
    assert get_upper_approximation(df, "Company", ["Mkt(a1)", "Dist(a3)"], "Sales(D)", "A") == {'C15', 'C19', 'C2', 'C7'}
    assert get_upper_approximation(df, "Company", ["Mkt(a1)", "Dist(a3)"], "Sales(D)", "L") == {'C1', 'C11', 'C12', 'C13', 'C14', 'C16', 'C17', 'C18', 'C20', 'C21', 'C22', 'C23', 'C3', 'C4', 'C5', 'C6', 'C8', 'C9'}

def test_get_upper_approximation_example3():
    """
        以範例3測試 get_upper_approximation
        
    """
    
    df = pd.read_csv("Blood_disease.csv")
    
    assert get_upper_approximation(df, "Sample", ["Blood type"], "Disease", 1) == {1, 2, 3, 4, 5, 7}