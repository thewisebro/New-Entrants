#!/bin/bash
cd /home/apps/channeli_media/news/xml_files

<<COMMENT
NOTE:
  "wget -U firefox http://www.abcxyz.com/bla/bla/"
  '-U' means 'User Agent' which is 'firefox' in our context.
  We need to add this additional parameter while using wget why b'coz
  there is a possibility that a site owner can block access for downloading content
  for all user agents(Which gives an error code 403:FORBIDDEN) except for the browser agent.
COMMENT

#The Hndu
wget -U firefox "http://www.thehindu.com/news/international/?service=rss";
mv "index.html?service=rss" hindu_int.xml
wget -U firefox "http://www.thehindu.com/news/national/?service=rss";
mv "index.html?service=rss" hindu_nat.xml
wget -U firefox "http://www.thehindu.com/sport/?service=rss";
mv "index.html?service=rss" hindu_sports.xml
wget -U firefox "http://www.thehindu.com/features/?service=rss";
mv "index.html?service=rss" hindu_entertainment.xml
wget -U firefox "http://www.thehindu.com/features/?service=rss";
mv "index.html?service=rss" hindu_science_tech.xml
#wget "http://www.thehindu.com/features/?service=rss";
#mv "index.html?service=rss" hindu_tech.xml
wget -U firefox "http://www.thehindu.com/features/education/?service=rss";
mv "index.html?service=rss" hindu_education.xml
wget -U firefox "http://www.thehindu.com/sci-tech/health/?service=rss";
mv "index.html?service=rss" hindu_health.xml

#Times of India
wget -U firefox "http://timesofindia.feedsportal.com/c/33039/f/533917/index.rss";
mv "index.rss" toi_int.xml
wget -U firefox "http://timesofindia.feedsportal.com/c/33039/f/533916/index.rss";
mv "index.rss" toi_nat.xml
wget -U firefox "http://timesofindia.feedsportal.com/c/33039/f/533921/index.rss";
mv "index.rss" toi_sports.xml
wget -U firefox "http://timesofindia.feedsportal.com/c/33039/f/533928/index.rss";
mv "index.rss" toi_entertainment.xml
wget -U firefox "http://timesofindia.feedsportal.com/c/33039/f/533922/index.rss";
mv "index.rss" toi_science.xml
wget -U firefox "http://timesofindia.feedsportal.com/c/33039/f/533923/index.rss";
mv "index.rss" toi_tech.xml
wget -U firefox "http://timesofindia.feedsportal.com/c/33039/f/533924/index.rss";
mv "index.rss" toi_education.xml
wget -U firefox "http://timesofindia.feedsportal.com/c/33039/f/533968/index.rss";
mv "index.rss" toi_health.xml

#Indian Express: OLD FEED LINKS
#wget "http://syndication.indianexpress.com/rss/798/latest-news.xml";
#wget "http://syndication.indianexpress.com/rss/789/latest-news.xml"
#wget "http://syndication.indianexpress.com/rss/785/latest-news.xml";

#Indian Express: NEWLY UPDATED FEED LINKS
wget -U firefox "http://indianexpress.com/section/world/feed/"
mv "index.html" ie_int.xml
wget -U firefox "http://indianexpress.com/section/india/feed/"
mv "index.html" ie_nat.xml
wget -U firefox "http://indianexpress.com/section/sports/feed/"
mv "index.html" ie_sports.xml
wget -U firefox "http://indianexpress.com/section/entertainment/feed/"
mv "index.html" ie_entertainment.xml
wget -U firefox "http://indianexpress.com/section/technology/feed/"
mv "index.html" ie_science.xml
wget -U firefox "http://indianexpress.com/section/india/education/feed/"
mv "index.html" ie_education.xml
wget -U firefox "http://indianexpress.com/section/lifestyle/health/feed/"
mv "index.html" ie_health.xml

<<COMMENT
#Hindustan Times
wget "http://feeds.hindustantimes.com/HT-WorldSectionPage-Topstories";
mv "HT-WorldSectionPage-Topstories" ht_int.xml
wget "http://feeds.hindustantimes.com/HT-IndiaSectionPage-Topstories";
mv "HT-IndiaSectionPage-Topstories" ht_nat.xml
wget "http://feeds.hindustantimes.com/HT-SportsSection-Topstories";
mv "HT-SportsSection-Topstories" ht_sports.xml
wget "http://feeds.hindustantimes.com/HT-HomePage-Entertainment";
mv "HT-HomePage-Entertainment" ht_entertainment.xml
COMMENT

#Msn News
wget -U firefox "http://news.in.msn.com/rss/world_news.aspx"
mv "world_news.aspx" msn_int.xml
wget -U firefox "http://news.in.msn.com/rss/india_news.aspx"
mv "india_news.aspx" msn_nat.xml
wget -U firefox "http://sports.in.msn.com/rss/cricket_news.aspx"  # Includes only 'cricket' news
mv "cricket_news.aspx" msn_sports.xml
wget -U firefox "http://entertainment.in.msn.com/rss/hollywood.aspx"  # Provides Bollywood news also..
mv "hollywood.aspx" msn_entertainment.xml

#Yahoo News
wget -U firefox "http://in.news.yahoo.com/rss/world"
mv "world" yahoo_int.xml
wget -U firefox "http://in.news.yahoo.com/rss/national"
mv "national" yahoo_nat.xml
wget -U firefox "http://in.news.yahoo.com/rss/sports"
mv "sports" yahoo_sports.xml

<<COMMENT
#Google-News
wget "http://news.google.co.in/news?pz=1&cf=all&ned=in&hl=en&topic=w&output=rss";
mv "news?pz=1&cf=all&ned=in&hl=en&topic=w&output=rss" google_int.xml
wget "http://news.google.co.in/news?pz=1&cf=all&ned=in&hl=en&topic=n&output=rss";
mv "news?pz=1&cf=all&ned=in&hl=en&topic=n&output=rss" google_nat.xml
wget "http://news.google.co.in/news?pz=1&cf=all&ned=in&hl=en&topic=s&output=rss";
mv "news?pz=1&cf=all&ned=in&hl=en&topic=s&output=rss" google_sports.xml
COMMENT

#BBC-International
wget -U firefox "http://feeds.bbci.co.uk/news/world/rss.xml";
mv "rss.xml" bbc_int.xml
wget -U firefox "http://feeds.bbci.co.uk/news/world/asia/india/rss.xml";
mv "rss.xml" bbc_nat.xml
wget -U firefox "http://feeds.bbci.co.uk/sport/0/rss.xml?edition=uk";
mv "rss.xml?edition=uk" bbc_sports.xml
wget -U firefox "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml";
mv "rss.xml" bbc_entertainment.xml
wget -U firefox "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml";
mv "rss.xml" bbc_science.xml
wget -U firefox "http://feeds.bbci.co.uk/news/technology/rss.xml";
mv "rss.xml" bbc_tech.xml
wget -U firefox "http://feeds.bbci.co.uk/news/health/rss.xml";
mv "rss.xml" bbc_health.xml

#Additional RSS links - BBC
wget -U firefox "http://feeds.bbci.co.uk/sport/0/cricket/rss.xml?edition=uk";
mv "rss.xml?edition=uk" cricket.xml
wget -U firefox "http://feeds.bbci.co.uk/sport/0/football/rss.xml?edition=uk";
mv "rss.xml?edition=uk" football.xml
wget -U firefox "http://feeds.bbci.co.uk/sport/0/tennis/rss.xml?edition=uk";
mv "rss.xml?edition=uk" tennis.xml

<<COMMENT
#Newyork Times
wget "http://feeds.nytimes.com/nyt/rss/World";
mv "World" nyt_int.xml
wget "http://topics.nytimes.com/topics/reference/timestopics/subjects/b/badminton/index.html?rss=1";
mv "index.html?rss=1" badminton.xml
wget "http://topics.nytimes.com/topics/reference/timestopics/subjects/c/chess/index.html?rss=1";
mv "index.html?rss=1" chess.xml
COMMENT

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

