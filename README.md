# Brand Sentiment

A set of scripts that makes sentiment analysis of your brand
based on Google News and Twitter news streams. It utilizes Heartex
platform to create a custom neural network to do the study
specifically for your brand

[http://heartex.net/](Tutorial)

# Run it for your own brand

! Important. To make it work you need to obtain **Heartex token**, to
do so [http://heartex.net/business/signup/?ref=github](register
here). We give you a free account with 10k API requests (with above
link only!).

```sh
# install

```

```sh
# configure
export TOKEN=""
export BRAND=""
```

```sh
# first we need to grab news data
python src/get_google_news.py --pages=10 --query=$BRAND --output=news.csv
```

```sh
# create Heartex project to filter news that are only relevent to your company

# you will get back a link where you need to train a neural network a little bit to make it understand what is relevent to you
python src/create_filter_project.py --token=$TOKEN --input=news.csv

export FILTER_PROJECT=""
```

```sh
# get predictions
python src/predict_and_filter.py --project=$FILTER_PROJECT --token=$TOKEN --output=filtered.csv
```

```sh
# 
python src/create_sentiment_project.py --token=$TOKEN --input=filtered.csv

export SENTIMENT_PROJECT=""
```

```sh
# 
python src/add_sentiment_chart.py --token=$TOKEN --project=$SENTIMENT_PROJECT --input=filtered.csv
```

```sh

```
