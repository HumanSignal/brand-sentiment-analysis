# Brand Sentiment

A set of scripts that makes sentiment analysis of your brand
based on Google News and Twitter news streams. It utilizes Heartex
platform to create a custom neural network to do the study
specifically for your brand

[Tutorial](https://heartex.net/use-case/sentiment)

# Installation 

! Important. To make it work you need to obtain **Heartex token**, to
do so [signup here](https://go.heartex.net/business/signup/?ref=github). We give you a free account with 10k API requests (with above
link only!).

```sh
# install

```

```sh
# configure
export TOKEN=""
export BRAND=""
```

# Run it for your own brand

```sh
# first we need to grab news data
python src/get_google_news.py --pages=10 --query=$BRAND --output=news.csv
```

```sh
# 
python src/create_sentiment_project.py --token=$TOKEN --input=news.csv

export SENTIMENT_PROJECT=""
```

```sh
# predict dataset and save it's sentiment 
python src/add_sentiment_chart.py --token=$TOKEN --project=$SENTIMENT_PROJECT --input=news.csv --results=$BRAND

# open sentiment html
firefox $BRAND/index.html
```
?ref=github
# Filter Results First

In case your brand may appear in different contexts, for example, with
the name of one of your products (ex: Apple Watch), you may want to
filter those occurrences first. 

To do that we will use another type of model which is called a tagger
model. It learns when you tag relevant occurrences.

```sh
PRODUCTS="Apple,iOS,iPadOS,watchOS,macOS,MacPro,Pro Display"
```

```sh
# create Heartex project to filter news that are only relevent to your brand name

# you will get back a link where you need to train a neural network a little bit to make it understand what is relevent to you
python src/create_filter_project.py --token=$TOKEN --input=news.csv --labels=$PRODUCTS

# set project here
export FILTER_PROJECT=""
```

```sh
# get predictions
python src/predict_and_filter.py --project=$FILTER_PROJECT --token=$TOKEN --output=filtered.csv --filter-labels=$PRODUCTS
```

Now you have filtered.csv which you can use for further sentiment
analysis.
