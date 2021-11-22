```python
import seaborn as sns
import matplotlib.pyplot as plt
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
```


```python
df = pd.read_csv('ProcessedTexts.csv', index_col='ROWID')
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 855 entries, 153251 to 130705
    Data columns (total 24 columns):
     #   Column            Non-Null Count  Dtype  
    ---  ------            --------------  -----  
     0   Unnamed: 0        855 non-null    int64  
     1   SenderPhonNumber  855 non-null    int64  
     2   Sender            855 non-null    object 
     3   text              855 non-null    object 
     4   attributedBody    855 non-null    object 
     5   type              855 non-null    int64  
     6   date              855 non-null    float64
     7   timestamp         855 non-null    object 
     8   month_name        855 non-null    object 
     9   day_name          855 non-null    object 
     10  day               855 non-null    int64  
     11  hour              855 non-null    int64  
     12  weekday           855 non-null    int64  
     13  week              855 non-null    int64  
     14  year              855 non-null    int64  
     15  polarity          855 non-null    float64
     16  subjectivity      855 non-null    float64
     17  negativity        855 non-null    float64
     18  neutrality        855 non-null    float64
     19  positivity        855 non-null    float64
     20  compound          855 non-null    float64
     21  nouns             855 non-null    object 
     22  tags              855 non-null    object 
     23  word_count        855 non-null    int64  
    dtypes: float64(7), int64(9), object(8)
    memory usage: 167.0+ KB



```python
df['month_year'] = pd.to_datetime(df['month_name'] + ' ' + df['year'].astype(str))
```


```python
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 1.5})
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
f, axs = plt.subplots(2,2, figsize=(36,25), gridspec_kw=dict(width_ratios=[4, 4]))
error_style = 'band'
confidence = 25
sns.lineplot(x='month_year', y='positivity', hue='Sender', style='Sender', err_style=error_style, ci=confidence, data=df, ax=axs[0,0]).set(title="Positive Sentiment of Texts", ylabel=None, xlabel=None)
for tick in axs[0,0].get_xticklabels():
    tick.set_rotation(55)
sns.lineplot(x='month_year', y='negativity', hue='Sender', style='Sender', err_style=error_style, ci=confidence, data=df, ax=axs[0,1]).set(title="Negative Sentiment of Texts", ylabel=None, xlabel=None)
for tick in axs[0,1].get_xticklabels():
    tick.set_rotation(55)
sns.lineplot(x='month_year', y='word_count', hue='Sender', style='Sender', err_style=error_style, ci=confidence, data=df, ax=axs[1,0]).set(title="Word Counts of Texts", ylabel=None, xlabel='Month')
for tick in axs[1,0].get_xticklabels():
    tick.set_rotation(55)
sns.lineplot(x='month_year', y='compound', hue='Sender', style='Sender', err_style=error_style, ci=confidence, data=df, ax=axs[1,1]).set(title="Complexity of Texts", ylabel=None, xlabel='Month')
for tick in axs[1,1].get_xticklabels():
    tick.set_rotation(55)
```


![png](output_3_0.png)



```python
sns.kdeplot(df['compound'])
```




    <AxesSubplot:xlabel='compound', ylabel='Density'>




![png](output_4_1.png)



```python
def generate_word_cloud(sender): 
    nouns = ""
    sdf = df[df['Sender'] == sender]
    for text in sdf['text']:
        for noun in TextBlob(text).noun_phrases: 
            nouns += f" {noun}"
    # Create the wordcloud object
    pass_list = ['corey', 'stop2end', 'stop2quit', 'recipient name', 'recipient  name', '< recipient name >', 'bit', 'ly', 'name', 'recipient']
    wordcloud = WordCloud(width=8000, height=4600, background_color="white", stopwords=pass_list, margin=2).generate(nouns)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.show()
```


```python
generate_word_cloud('Trump')
```


![png](output_6_0.png)



```python
generate_word_cloud('Biden')
```


![png](output_7_0.png)



```python
generate_word_cloud('Warnock')
```


![png](output_8_0.png)



```python
sns.kdeplot(df['word_count'])
```




    <AxesSubplot:xlabel='word_count', ylabel='Density'>




![png](output_9_1.png)



```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 861 entries, 153251 to 130705
    Data columns (total 25 columns):
     #   Column            Non-Null Count  Dtype         
    ---  ------            --------------  -----         
     0   Unnamed: 0        861 non-null    int64         
     1   SenderPhonNumber  861 non-null    int64         
     2   Sender            861 non-null    object        
     3   text              861 non-null    object        
     4   attributedBody    861 non-null    object        
     5   type              861 non-null    int64         
     6   date              861 non-null    float64       
     7   timestamp         861 non-null    object        
     8   month_name        861 non-null    object        
     9   day_name          861 non-null    object        
     10  day               861 non-null    int64         
     11  hour              861 non-null    int64         
     12  weekday           861 non-null    int64         
     13  week              861 non-null    int64         
     14  year              861 non-null    int64         
     15  polarity          861 non-null    float64       
     16  subjectivity      861 non-null    float64       
     17  negativity        861 non-null    float64       
     18  neutrality        861 non-null    float64       
     19  positivity        861 non-null    float64       
     20  compound          861 non-null    float64       
     21  nouns             861 non-null    object        
     22  tags              861 non-null    object        
     23  word_count        861 non-null    int64         
     24  month_year        861 non-null    datetime64[ns]
    dtypes: datetime64[ns](1), float64(7), int64(9), object(8)
    memory usage: 207.2+ KB



```python
f, axs = plt.subplots(2,2, figsize=(36,25), gridspec_kw=dict(width_ratios=[4, 4]))
colors = 'Set3'
sns.violinplot(x='Sender', y='neutrality', data=df, palette=colors, ax=axs[0,0]).set(title="Neutral Sentiment of Texts", ylabel=None, xlabel=None)
sns.violinplot(x='Sender', y='subjectivity', data=df, palette=colors, ax=axs[1,0]).set(title="Positive Sentiment of Texts", ylabel=None, xlabel=None)
sns.violinplot(x='Sender', y='negativity', data=df, palette=colors, ax=axs[0,1]).set(title="Negative Sentiment of Texts", ylabel=None, xlabel=None)
sns.violinplot(x='Sender', y='compound', data=df, palette=colors, ax=axs[1,1]).set(title="Complexity of Texts", ylabel=None, xlabel=None)
```




    [Text(0.5, 1.0, 'Complexity of Texts'), Text(0, 0.5, ''), Text(0.5, 0, '')]




![png](output_11_1.png)



```python
sns.barplot(y='day_name', x='word_count', data=df)
plt.xticks(rotation=45)
```




    (array([ 0., 10., 20., 30., 40.]),
     [Text(0, 0, ''),
      Text(0, 0, ''),
      Text(0, 0, ''),
      Text(0, 0, ''),
      Text(0, 0, '')])




![png](output_12_1.png)



```python
df[df['word_count'] == df['word_count'].max()]['text'].iloc[0]

```




    "￼<recipient name>, I'm the most vulnerable Senate Democrat up for reelection next year & I need your help: While my potential opponent Herschel Walker (R) is aligning himself with Trump & McConnell, I've spent my time in the Senate fighting for our progressive priorities. I'm in office to stand up to corrupt leaders & restore moral leadership to our government.\n\nPOLITICO says that Democrats' chances of defending our razor-thin majority hinge on keeping GA blue. Right now, we're running neck & neck with Walker - but while he's relying on GOP megadonors to try to buy this seat, I'm running a people-powered campaign. And unfortunately, with time running out before our mid-month deadline, we're falling short of our goal.\n\nThat's why I'm personally asking for your help today: Will you give $15 or more now so we can hit our mid-month goal, win in GA & defend our Senate majority? bit.ly/3qolzy5 - Rev. Warnock\n\nStop2End"




```python
df.sort_values('positivity', ascending=False)[['Sender', 'text', 'positivity']].head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Sender</th>
      <th>text</th>
      <th>positivity</th>
    </tr>
    <tr>
      <th>ROWID</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>144200</th>
      <td>Trump</td>
      <td>HELP</td>
      <td>1.000</td>
    </tr>
    <tr>
      <th>132221</th>
      <td>Biden</td>
      <td>YES</td>
      <td>1.000</td>
    </tr>
    <tr>
      <th>142979</th>
      <td>Trump</td>
      <td>All true</td>
      <td>0.737</td>
    </tr>
    <tr>
      <th>134996</th>
      <td>Trump</td>
      <td>￼President Trump: On behalf of our wonderful F...</td>
      <td>0.506</td>
    </tr>
    <tr>
      <th>134744</th>
      <td>Trump</td>
      <td>The President has a special CHRISTMAS GIFT for...</td>
      <td>0.471</td>
    </tr>
    <tr>
      <th>150496</th>
      <td>Trump</td>
      <td>WOW!\n\nPresident Trump AND Herschel Walker si...</td>
      <td>0.456</td>
    </tr>
    <tr>
      <th>149718</th>
      <td>Trump</td>
      <td>WOW!\n\nPresident Trump AND Herschel Walker si...</td>
      <td>0.456</td>
    </tr>
    <tr>
      <th>134126</th>
      <td>Trump</td>
      <td>Pres. Trump: On behalf of the Trump Family, I ...</td>
      <td>0.454</td>
    </tr>
    <tr>
      <th>136444</th>
      <td>Biden</td>
      <td>Jaime here! You donated generously last month,...</td>
      <td>0.429</td>
    </tr>
    <tr>
      <th>138630</th>
      <td>Biden</td>
      <td>DNC HQ: Interested in getting special updates ...</td>
      <td>0.428</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.sort_values('negativity', ascending=False)[['Sender', 'text', 'negativity']].head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Sender</th>
      <th>text</th>
      <th>negativity</th>
    </tr>
    <tr>
      <th>ROWID</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>144198</th>
      <td>Trump</td>
      <td>Sad trump noises</td>
      <td>0.608</td>
    </tr>
    <tr>
      <th>147798</th>
      <td>Trump</td>
      <td>Pres Trump: Biden just went on TV &amp; blamed ME ...</td>
      <td>0.435</td>
    </tr>
    <tr>
      <th>142972</th>
      <td>Trump</td>
      <td>MADMAN\nLUNATIC\nRACIST\nCORRUPT\n\n^ that's w...</td>
      <td>0.296</td>
    </tr>
    <tr>
      <th>135250</th>
      <td>Trump</td>
      <td>Pres Trump: Is it true that voting machines 's...</td>
      <td>0.292</td>
    </tr>
    <tr>
      <th>134015</th>
      <td>Trump</td>
      <td>Pres Trump &amp; VP Pence: It's so urgent we BOTH ...</td>
      <td>0.276</td>
    </tr>
    <tr>
      <th>148821</th>
      <td>Trump</td>
      <td>Pres Trump: I've said it once and I'll say it ...</td>
      <td>0.275</td>
    </tr>
    <tr>
      <th>152670</th>
      <td>Trump</td>
      <td>'20 FRAUD?\n'21 DO NOTHING TO FIX\n'22 WE LOSE...</td>
      <td>0.273</td>
    </tr>
    <tr>
      <th>149548</th>
      <td>Trump</td>
      <td>"This is not about freedom"\n\nThat's what Bid...</td>
      <td>0.259</td>
    </tr>
    <tr>
      <th>145027</th>
      <td>Trump</td>
      <td>Don Jr: Our FEC Deadline is TOMORROW. If we do...</td>
      <td>0.240</td>
    </tr>
    <tr>
      <th>134291</th>
      <td>Trump</td>
      <td>FINAL NOTICE! Pres Trump EXTENDED your 1000% O...</td>
      <td>0.239</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
