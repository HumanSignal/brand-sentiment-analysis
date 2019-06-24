# Brand Sentiment

A set of scripts that makes sentiment analysis of your brand
based on Google News and Twitter news streams. It utilizes Heartex
platform to create a custom neural network to do the study
specifically for your brand

[Tutorial](https://heartex.net/use-case/sentiment)

![](https://github.com/heartexlabs/brand-sentiment-analysis/raw/master/demo.png)

# Installation 

> Important. To make it work you need to obtain **Heartex token**, to do so [signup here](https://go.heartex.net/business/signup/?ref=github). We give you a free account with 10k API requests (with above
link only!).

```sh
# install
python3 -m venv bsa-env
source bsa-env/bin/active
pip install -r requirements
```

```sh
# configure
export TOKEN=""
export BRAND=""
```

# Create Sentiment Model

```sh
# first we need to grab news data
python src/get_google_news.py --pages=10 --query=$BRAND --output=news.csv
```

```sh
#  create project on heartex
python src/create_sentiment_project.py --token=$TOKEN --input=news.csv

# you will get project id, save it here
export SENTIMENT_PROJECT_ID=""
```

Open up `src/config.json` and put **$TOKEN** and **$SENTIMENT_PROJECT_ID** there

# Run

Execute ``` python3 service.py config.json```

# Add your own data

> [TBD]

# Advanced: Filter Results

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

Now you have what is called a smart filter, edit config.json and include it there. You will see smart filter buttons on the index page.
