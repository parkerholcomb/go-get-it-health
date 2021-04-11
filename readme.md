# About gogetit.health

For the past couple months, 👋🏾 Dwamian, Scott, and I have been working on a way to help, and today we're finally able to release our our #gogetit bot.

If you're looking for #covid #vaccine availability in #Texas, just text your zip code to 512-409-9745 or visit https://gogetit.health to get started.

It started with "How can I find my Dad the next available vaccine". Refreshing dozens of websites wasn't going to cut it, I wanted to get a push notification as soon as supply became available. After he got his vaccine in March, this morphed into "how can we get out this information out to people as simply as possible".

We are now actively tracking almost 4,000 locations across Texas for supply updates (through the Texas Department of Emergency Management), and if there's updated availability within 50 miles of your zip code, you'll be the first to know.

Y'all - the time is now to lean in, advocate for your health and the health of your community, and #gogetit.

![](https://vaccinate-texas-public.s3.amazonaws.com/vaccinate-texas-og-img.png)

# About this project

This project contains two serverless projects

## cloud_functions
Python Lambda functions deployed with Serverless Framework 2

These borrow from a Lambda layer which contains my three core utiliites for this project:
- pandas 
- geopy 
- twilio

### Core Python Classes `lib/` 
- Fetcher: grabs data at recurring rate (we at 30 min right now)
- Loader: Computes the changeset of the current and last data snapshot, returns updates_df
- GeoZipCache: computes distances at zip to to zip granularity
- Messager: SMS Wrapper
- Subscriber: subscribers at stored

## site

React app deployed with Serverless Components

