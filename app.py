import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_tweet_preview(tweet_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(tweet_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', {'property': 'og:description'})
        if meta_tag and meta_tag.get('content'):
            return meta_tag.get('content')
        tweet_div = soup.find('div', {'data-testid': 'tweetText'})
        if tweet_div:
            return tweet_div.get_text(separator=' ', strip=True)
        return "Could not extract tweet text."
    except Exception as e:
        return f"Error: {e}"

st.title("Tweet Previewer")

option = st.radio("Choose input method:", ("Paste URLs", "Upload CSV"))

tweet_links = []

if option == "Paste URLs":
    st.write("Paste one tweet URL per line:")
    url_text = st.text_area("Tweet URLs", height=150)
    if url_text:
        tweet_links = [line.strip() for line in url_text.splitlines() if line.strip()]
elif option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file with a column named 'url'")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'url' in df.columns:
            tweet_links = df['url'].dropna().tolist()
        else:
            st.error("CSV must have a column named 'url'.")

if tweet_links:
    st.write("## Tweet Previews")
    previews = []
    for url in tweet_links:
        preview = get_tweet_preview(url)
        previews.append({'URL': url, 'Preview': preview})
    st.dataframe(pd.DataFrame(previews))
