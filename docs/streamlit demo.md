# Roughset Streamlit Cloud 使用說明

## Step0-開啟應用

開啟[Roughset App](https://roughset.streamlit.app/)

![](https://i.imgur.com/DAclnOH.png)

## Step1-上傳資料
資料的格式必須是csv檔，包含
+ 一個欄位為**名稱**欄位(不可重複)
+ 一個欄位為**決策屬性**欄位
+ 其他欄位為**特徵屬性**欄位

> 格式可參考[example.csv](https://github.com/Keycatowo/rough-set/blob/main/test/example.csv)

![](https://i.imgur.com/RtWVZFS.png)

## Step2-決定欄位
+ 預設為
    + 第一個欄位為**名稱**欄位
    + 最後欄位為**決策屬性**欄位
    + 其餘欄位為**特徵屬性**欄位
+ 可以自行調整

![](https://i.imgur.com/dV9TfUj.png)

## Step3-計算約略集規則
點擊**計算約略集規則**按鈕，即可計算約略集規則

![](https://i.imgur.com/f1cMl2Y.png)


## Step4-篩選規則
+ 若所有的特徵屬性欄位為**X**，決策欄位為**Y**

### 設定支持度(Support)門檻
+ Support定義：
    + 規則的支持度 = 這條規則相同的X的數量 / 所有資料數
    + Support = P(X)
+ Support越大表示規則越常出現，反之則越不常出現

![](https://i.imgur.com/cZXbH3r.png)

### 設定信賴度(Confidence)門檻
+ Confidence定義：
    + 規則的信賴度 = 與這條規則相同X且相同Y的資料數量 / 與這條規則相同X的資料數量
    + Confidence = P(Y|X)
+ 信賴度越大表示此規則在此資料集中的正確率越高

![](https://i.imgur.com/zWRkVaX.png)

### 設定增益(lift)門檻
+ Lift定義：
    + 規則的增益 = 與這條規則相同X且相同Y的資料數量 / (與這條規則相同X的資料數量 * 與這條規則相同Y的資料數量)
    + Lift = P(Y|X) / P(Y)
+ lift越大表示從這筆資料中得到的資訊越多，反之則越少

![](https://i.imgur.com/kyH568e.png)

### 去除重複規則(Deduplicate)
+ 預設生成結果會記錄包含這個規則來自哪筆資料
+ 勾選此選項後，會去除重複的規則(只保留一筆)，同時移除來自哪筆資料的資訊

#### 去除重複規則前
![](https://i.imgur.com/SHFq6lE.png)

#### 去除重複規則後
![](https://i.imgur.com/38bkNya.png)
