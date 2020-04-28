import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from textblob import TextBlob
import nltk

data = pd.read_csv("OnlineNewsPopularity.csv")

data = data.drop(['url','timedelta', 'LDA_00','LDA_01','LDA_02','LDA_03','LDA_04','num_self_hrefs','num_videos', 'kw_min_min', 'kw_max_min', 'kw_avg_min','kw_min_max','kw_max_max','kw_avg_max','kw_min_avg','kw_max_avg','kw_avg_avg','self_reference_min_shares','self_reference_max_shares','self_reference_avg_sharess','rate_positive_words','rate_negative_words','abs_title_subjectivity','abs_title_sentiment_polarity','data_channel_is_lifestyle','data_channel_is_entertainment','data_channel_is_bus','data_channel_is_socmed','data_channel_is_tech','data_channel_is_world','weekday_is_monday','weekday_is_tuesday','weekday_is_wednesday','weekday_is_Thursday','weekday_is_friday','weekday_is_saturday','weekday_is_sunday','is_weekend','num_imgs','num_hrefs','n_unique_tokens','n_non_stop_words','n_non_stop_unique_tokens','average_token_length','num_keywords','global_rate_positive_words','global_rate_negative_words','avg_positive_polarity','min_positive_polarity','max_positive_polarity','max_negative_polarity','min_negative_polarity','avg_negative_polarity'], axis=1)
print(data.info())


X = data.drop('shares', axis=1)
y = data['shares'] 

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state=1)


#Random Forest
rand = RandomForestRegressor() 

# fit the regressor with x and y data 
rand.fit(X_test,y_test)  
rand_pred = rand.predict(X_test) 

accuracy1 = rand.score(X_test,y_test)
print("Accuracy of RandomForest ",accuracy1*100,'%')


#Scrapped data

Scrap_data = pd.read_csv('news.csv', index_col=0)
Scrap_data = Scrap_data.drop(['link'], axis=1)


news_data = pd.DataFrame(data=Scrap_data)
print(news_data)
#Find polarity
news_data['title_sentiment_polarity'] = news_data.apply(lambda x: TextBlob(x['Title']).sentiment.polarity, axis=1)

news_data['global_sentiment_polarity'] = news_data.apply(lambda x: TextBlob(x['Article']).sentiment.polarity, axis=1)

#Find subjectivity
news_data['title_subjectivity'] = news_data.apply(lambda x: TextBlob(x['Title']).sentiment.subjectivity, axis=1)
news_data['global_subjectivity'] = news_data.apply(lambda x: TextBlob(x['Article']).sentiment.subjectivity, axis=1)


#number of words in title
title = news_data['Title'].str.split().str.len()
news_data['n_tokens_title'] = title
 
#number of words in Article
article = news_data['Article'].str.split().str.len()
news_data['n_tokens_content'] = article

print(news_data)
pred_data = pd.DataFrame(news_data)
pred_test=pred_data.drop(['Title','description','Article','Tags'],axis=1)

predict=pd.DataFrame(rand.predict(pred_test),pred_data['Title'])
predict.reset_index(level=0, inplace=True)
predict = predict.rename(columns={"index": "Title", 0: "Shares"})
print(predict)

predict.plot(figsize=(16,10))
plt.xlabel("Title number(0-going)")
plt.ylabel("Shares")
plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
plt.show()