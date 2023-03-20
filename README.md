# 🐍 Rough Set Python Package

Rough Set Python Package is a Python library that provides a set of tools to calculate rough sets and obtain reduct rules. This package is useful for data analysis and machine learning tasks where you need to deal with uncertainty or incomplete data.

![](fig/%E7%B4%84%E7%95%A5%E9%9B%86%E5%90%88(rough%20set)%20%E9%96%8B%E7%99%BC.png)
## 📦 Installation
You can install Rough Set Python Package using pip command:

```bash
pip install roughset
```

## 📚 Usage
With a example data
![Example data](https://i.imgur.com/AHzxjiu.png)

```python
from roughset.reduct import create_reduct_rules

# Load data from a CSV file
df = pd.read_csv('example.csv')

# Calculate reduct rules
create_reduct_rules(
    df=df,
    name_col="No",
    feature_col=['天氣', '事故情形', '事故原因'],
    decision_col='損壞部位',
    include_empty=True # Include empty reduct rules
)
```
We will get the reduct rules.
![reduct rules result](https://i.imgur.com/wyG1wUr.png)



## 🤝 Contribution
If you want to contribute to Rough Set Python Package, you can fork the repository on GitHub and create a pull request. You can also report bugs, suggest new features, or ask for help in the issues section.

## 📜 License

Rough Set Python Package is released under the MIT License. You can find the details of the license in the `LICENSE` file.