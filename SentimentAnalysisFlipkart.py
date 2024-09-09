import streamlit as st
import requests as rq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import re
import nltk
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")    #earlier used "agg" backend that didnt work with streamlit
import string
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

def clean_text(text):
    cleaned_text = re.sub('<.*?>', '', text)   
    cleaned_text = cleaned_text.translate(str.maketrans('', '', string.punctuation))   
    cleaned_text = re.sub(r'\d+', '', cleaned_text)   
    cleaned_text = ' '.join(cleaned_text.split())    
    cleaned_text = cleaned_text.lower()       
    return cleaned_text

def webScrapingReviews(url):
    reviews = []                          # Initialize an empty list to store reviews
    link = []
    
    r1 = rq.get(url)
    sleep(2)                        
    soup1 = BeautifulSoup(r1.text, 'html.parser')
    
    f_url = ''
    # Step 2: Find and construct the URL for the product reviews page
    for i in soup1.findAll('a', attrs={'href': re.compile("/product-review")}):
        q = i.get('href')
        link.append(q)                      # Append the href value to the link list
        for j in link:
            if 'LSTMOBF3HZ2H9YZSYRYTFKW51' in j:
                aa = i
        f_url = 'https://www.flipkart.com' + str(j)
    
    # Step 3: Set up Selenium WebDriver to navigate through review pages
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Run in headless mode

    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'  # Adjust this path as needed
    chrome_options.binary_location = chrome_path
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f_url)
    
    i = 1
    # Step 4: Iterate through 2 pages of reviews
    while i < 3:
        ss = driver.get(f_url + "&page=" + str(i))
        qq = driver.current_url
        r2 = rq.get(qq)
        soup = BeautifulSoup(r2.text, 'html.parser')

        # Step 5: Extract reviews from the reviews container
        reviews_container = soup.find('div', {'class': '_1YokD2 _3Mn1Gg col-9-12'})
        if reviews_container:
            reviews_divs = reviews_container.find_all('div', {'class': 't-ZTKy'})
            for child in reviews_divs:
                third_div = child.div.div                       
                text = third_div.text.strip()                    # Extract text from review div
                cleaned_text = clean_text(text)                 # Clean the extracted text using the clean_text function
                reviews.append(cleaned_text)                     # Append cleaned text to the reviews list
        else:
            print(f"No reviews container found on page {i}")
        sleep(1)                                  # Pause for 1 second before navigating to the next page
        i += 1
    
    driver.quit()  # Close the browser
    file_path='reviews2.xlsx'
    data = pd.DataFrame({'review': reviews})
    data.to_excel(file_path, index=False)
    
  
    return data

def sentimentAnalysis(data):
    sid = SentimentIntensityAnalyzer()                  # Initialize SentimentIntensityAnalyzer from NLTK
    def sentiment_vader(text):
        over_all_polarity = sid.polarity_scores(text)         # Compute sentiment polarity scores
        if over_all_polarity['compound'] >= 0.05:
            return 'positive'
        elif over_all_polarity['compound'] < -0.05:
            return 'negative'
        else:
            return 'neutral'
    file_path='sentiment_result.xlsx' 
    data['polarity'] = data['review'].apply(lambda review: sentiment_vader(review))    # Apply sentiment analysis function
    data.to_excel('sentiment_result.xlsx', index=False)
    

def visualization():
    file = pd.read_excel('sentiment_result.xlsx')          # Read sentiment analysis results from Excel file

    st.write("Loaded Sentiment Data:")
    st.dataframe(file.head())                               # Display the first few rows of the DataFrame in Streamlit
    
    total_labels = len(file['polarity'])
    label_counts = pd.Series(file['polarity']).value_counts()         # Count occurrences of each sentiment
    percentages = (label_counts / total_labels) * 100                   # Calculate percentages of each sentiment
    print(percentages)

    fig, ax = plt.subplots()                                           # Create pie chart plot
    ax.pie(percentages, labels=percentages.index, autopct='%1.1f%%', startangle=90)      # Plot pie chart

    ax.set_aspect('equal')  # Ensure pie is drawn as a circle
    st.pyplot(fig)







