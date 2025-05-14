import streamlit as st
import pandas as pd
import requests
import streamlit.components.v1 as components

def get_tweet_embed_html(tweet_url):
    api_url = f"https://publish.twitter.com/oembed?url={tweet_url}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()['html']
        else:
            return f"<p>Could not embed tweet: {tweet_url}</p>"
    except Exception as e:
        return f"<p>Error: {e}</p>"

st.title("Tweet Embedder")

option = st.radio("Choose input method:", ("Paste URLs", "Upload CSV"))

tweet_links = []

if option == "Paste URLs":
    url_text = st.text_area("Paste one tweet URL per line:")
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
    st.write("## Embedded Tweets")
    for i, url in enumerate(tweet_links):
        html = get_tweet_embed_html(url)

        copy_button_html = f"""
        <div style="margin-bottom: 40px;">
            <button onclick="navigator.clipboard.writeText('{url}'); alert('Copied to clipboard: {url}');" 
                    style="margin-bottom:10px; padding:6px 12px; cursor:pointer;">
                Copy Link
            </button>
            {html}
        </div>
        """

        components.html(copy_button_html, height=700)
