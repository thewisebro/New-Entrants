#!/bin/bash
cd /home/jagan/channeli/apps/news/xml_files

#The Hindu
wget "http://www.thehindu.com/news/international/?service=rss";
mv "index.html?service=rss" hindu_int.xml
wget "http://www.thehindu.com/news/national/?service=rss";
mv "index.html?service=rss" hindu_nat.xml
wget "http://www.thehindu.com/sport/?service=rss";
mv "index.html?service=rss" hindu_sports.xml
wget "http://www.thehindu.com/features/?service=rss";
mv "index.html?service=rss" hindu_entertainment.xml
wget "http://www.thehindu.com/features/?service=rss";
mv "index.html?service=rss" hindu_science_tech.xml
#wget "http://www.thehindu.com/features/?service=rss";
#mv "index.html?service=rss" hindu_tech.xml
wget "http://www.thehindu.com/features/education/?service=rss";
mv "index.html?service=rss" hindu_education.xml
wget "http://www.thehindu.com/sci-tech/health/?service=rss";
mv "index.html?service=rss" hindu_health.xml

#Times of India
wget "http://timesofindia.feedsportal.com/c/33039/f/533917/index.rss";
mv "index.rss" toi_int.xml
wget "http://timesofindia.feedsportal.com/c/33039/f/533916/index.rss";
mv "index.rss" toi_nat.xml
wget "http://timesofindia.feedsportal.com/c/33039/f/533921/index.rss";
mv "index.rss" toi_sports.xml
wget "http://timesofindia.feedsportal.com/c/33039/f/533928/index.rss";
mv "index.rss" toi_entertainment.xml
wget "http://timesofindia.feedsportal.com/c/33039/f/533922/index.rss";
mv "index.rss" toi_science.xml
wget "http://timesofindia.feedsportal.com/c/33039/f/533923/index.rss";
mv "index.rss" toi_tech.xml
wget "http://timesofindia.feedsportal.com/c/33039/f/533924/index.rss";
mv "index.rss" toi_education.xml
wget "http://timesofindia.feedsportal.com/c/33039/f/533968/index.rss";
mv "index.rss" toi_health.xml

#Indian Express: OLD FEED LINKS
#wget "http://syndication.indianexpress.com/rss/798/latest-news.xml";
#wget "http://syndication.indianexpress.com/rss/789/latest-news.xml"
#wget "http://syndication.indianexpress.com/rss/785/latest-news.xml";

#Indian Express: NEWLY UPDATED FEED LINKS
wget "http://indianexpress.com/section/world/feed/"
mv "index.html" ie_int.xml
wget "http://indianexpress.com/section/india/feed/"
mv "index.html" ie_nat.xml
wget "http://indianexpress.com/section/sports/feed/"
mv "index.html" ie_sports.xml
wget "http://indianexpress.com/section/entertainment/feed/"
mv "index.html" ie_entertainment.xml
wget "http://indianexpress.com/section/technology/feed/"
mv "index.html" ie_science.xml
wget "http://indianexpress.com/section/india/education/feed/"
mv "index.html" ie_education.xml
wget "http://indianexpress.com/section/lifestyle/health/feed/"
mv "index.html" ie_health.xml

#Hindustan Times
wget "http://feeds.hindustantimes.com/HT-WorldSectionPage-Topstories";
mv "HT-WorldSectionPage-Topstories" ht_int.xml
wget "http://feeds.hindustantimes.com/HT-IndiaSectionPage-Topstories";
mv "HT-IndiaSectionPage-Topstories" ht_nat.xml
wget "http://feeds.hindustantimes.com/HT-SportsSection-Topstories";
mv "HT-SportsSection-Topstories" ht_sports.xml
wget "http://feeds.hindustantimes.com/HT-HomePage-Entertainment";
mv "HT-HomePage-Entertainment" ht_entertainment.xml

#Msn News
wget "http://news.in.msn.com/rss/world_news.aspx"
mv "world_news.aspx" msn_int.xml
wget "http://news.in.msn.com/rss/india_news.aspx"
mv "india_news.aspx" msn_nat.xml
wget "http://sports.in.msn.com/rss/cricket_news.aspx"  # Includes only 'cricket' news
mv "cricket_news.aspx" msn_sports.xml
wget "http://entertainment.in.msn.com/rss/hollywood.aspx"  # Provides Bollywood news also..
mv "hollywood.aspx" msn_entertainment.xml

#Yahoo News
wget "http://in.news.yahoo.com/rss/world"
mv "world" yahoo_int.xml
wget "http://in.news.yahoo.com/rss/national"
mv "national" yahoo_nat.xml
wget "http://in.news.yahoo.com/rss/sports"
mv "sports" yahoo_sports.xml

#Google-News
wget "http://news.google.co.in/news?pz=1&cf=all&ned=in&hl=en&topic=w&output=rss";
mv "news?pz=1&cf=all&ned=in&hl=en&topic=w&output=rss" google_int.xml
wget "http://news.google.co.in/news?pz=1&cf=all&ned=in&hl=en&topic=n&output=rss";
mv "news?pz=1&cf=all&ned=in&hl=en&topic=n&output=rss" google_nat.xml
wget "http://news.google.co.in/news?pz=1&cf=all&ned=in&hl=en&topic=s&output=rss";
mv "news?pz=1&cf=all&ned=in&hl=en&topic=s&output=rss" google_sports.xml

#BBC-International
wget "http://feeds.bbci.co.uk/news/world/rss.xml";
mv "rss.xml" bbc_int.xml
wget "http://feeds.bbci.co.uk/news/world/asia/india/rss.xml";
mv "rss.xml" bbc_nat.xml
wget "http://feeds.bbci.co.uk/sport/0/rss.xml?edition=uk";
mv "rss.xml?edition=uk" bbc_sports.xml
wget "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml";
mv "rss.xml" bbc_entertainment.xml
wget "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml";
mv "rss.xml" bbc_science.xml
wget "http://feeds.bbci.co.uk/news/technology/rss.xml";
mv "rss.xml" bbc_tech.xml
wget "http://feeds.bbci.co.uk/news/health/rss.xml";
mv "rss.xml" bbc_health.xml

#Additional RSS links - BBC
wget "http://feeds.bbci.co.uk/sport/0/cricket/rss.xml?edition=uk";
mv "rss.xml?edition=uk" cricket.xml
wget "http://feeds.bbci.co.uk/sport/0/football/rss.xml?edition=uk";
mv "rss.xml?edition=uk" football.xml
wget "http://feeds.bbci.co.uk/sport/0/tennis/rss.xml?edition=uk";
mv "rss.xml?edition=uk" tennis.xml

#Newyork Times
wget "http://feeds.nytimes.com/nyt/rss/World";
mv "World" nyt_int.xml
wget "http://topics.nytimes.com/topics/reference/timestopics/subjects/b/badminton/index.html?rss=1";
mv "index.html?rss=1" badminton.xml
wget "http://topics.nytimes.com/topics/reference/timestopics/subjects/c/chess/index.html?rss=1";
mv "index.html?rss=1" chess.xml


<<COMMENT
mv "news?pz=1&cf=all&ned=in&hl=en&topic=w&output=rss" google_int.xml
mv "rss.xml" bbc_int.xml

mv "index.html?service=rss" hindu_int.xml
mv "index.html?service=rss.1" hindu_nat.xml
mv "index.html?service=rss.2" hindu_sports.xml
mv "index.html?service=rss.3" hindu_entertainment.xml

mv "World" nyt_int.xml

mv "index.rss" toi_nat.xml
mv "index.rss.1" toi_int.xml
mv "index.rss.2" toi_sports.xml 

#mv "latest-news.xml" ie_nat.xml
#mv "latest-news.xml.1" ie_int.xml
#mv "latest-news.xml.2" ie_sports.xml

mv "HT-WorldSectionPage-Topstories" ht_int.xml
mv "HT-IndiaSectionPage-Topstories" ht_nat.xml
mv "HT-SportsSection-Topstories" ht_sports.xml
mv "HT-HomePage-Entertainment" ht_entertainment.xml

mv "news?pz=1&cf=all&ned=in&hl=en&topic=n&output=rss" google_nat.xml
mv "news?pz=1&cf=all&ned=in&hl=en&topic=s&output=rss" google_sports.xml

mv "rss.xml?edition=uk" bbc_sports.xml
mv "rss.xml?edition=uk.1" cricket.xml
mv "rss.xml?edition=uk.2" football.xml
mv "rss.xml?edition=uk.3" tennis.xml
#mv "index.html?service=rss.2" hockey.xml
mv "index.html?rss=1" badminton.xml
mv "index.html?rss=1.1" chess.xml
COMMENT

