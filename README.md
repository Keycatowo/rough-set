# 🐍 Rough Set Python Package

[![pypi CI](https://github.com/Keycatowo/rough-set/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/Keycatowo/rough-set/actions/workflows/pypi-publish.yml) ![Commits](https://img.shields.io/github/commit-activity/m/Keycatowo/rough-set) ![Views](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FKeycatowo%2Frough-set&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Views&edge_flat=false) ![GitHub LICENSE](https://img.shields.io/github/license/Keycatowo/rough-set?style=plastic) ![GitHub repo size](https://img.shields.io/github/repo-size/Keycatowo/rough-set?style=plastic) ![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/Keycatowo/rough-set)  [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://roughset.streamlit.app/) [![pypi Downloads](https://static.pepy.tech/badge/roughset)](https://pypi.org/project/roughset/) [![pypi version](https://img.shields.io/pypi/v/roughset)](https://pypi.org/project/roughset/)

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
from roughset import RoughSet

# Load data from a CSV file
df = pd.read_csv('example.csv')

# Create RoughSet object
RS = RoughSet(
    df=df,
    name_col="No",
    feature_col=['天氣', '事故情形', '事故原因'],
    decision_col='損壞部位'
)
rules = RS.create_reduct_rules(include_empty=True)
rules
```
We will get the reduct rules.
![reduct rules result](https://i.imgur.com/wyG1wUr.png)


```python
rules_with_scores = RS.evaluate_metrics()
rules_with_scores
```
![](https://i.imgur.com/UjmomZj.png)


## 🤝 Contribution
If you want to contribute to Rough Set Python Package, you can fork the repository on GitHub and create a pull request. You can also report bugs, suggest new features, or ask for help in the issues section.

## 📜 License

Rough Set Python Package is released under the MIT License. You can find the details of the license in the `LICENSE` file.
