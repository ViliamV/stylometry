Toto je navod na:
1. Stahovanie tweetov z Twitteru
2. Klasifikaciu autora pomocou machine learningu metodou Bag of Words

1. Stahovanie
    1. Je potrebne ziskat Twitter API key, navod je na https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/.
    2. Vyplnit udaje do 01-twitter-API.txt (udaje ktore su tam teraz uz nefunguju)
    3. Do suboru 02-mena.txt vypisat uzivatelske mena (jedno na riadok) uzivatelov, ktorych tweety sa maju stiahnut (posledne v zozname je meno podozriveho autora)
    4. Nainstalovat Python3, Tweepy (https://github.com/tweepy/tweepy)
    5. Spustit 03-tweet-download.py
    
2. Klasifikacia
    1. Nainstalovat Python3, nltk, numpy, scipy, unidecode (https://pypi.python.org/pypi/Unidecode), sklearn
    2. Upravit v 04-classification.py konstantu PODOZRIVY (riadok 30) na meno podozriveho uctu
    3. Spustit 04-classification.py (vystup je v cmd)
    
    Vystupom je klasifikacia jednotlivych balikov podozriveho, je vhodne proces opakovat viac krat.
    Cislo (vo vystupe klasifikacie) odpoveda vyssie uvedenemu poradiu v zozname mien.
