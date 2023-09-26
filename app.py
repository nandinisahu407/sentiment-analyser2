import time
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from pytube import YouTube
from googleapiclient.discovery import build
import re
import pandas as pd
import os
import emoji
import Csv_to_text
import numpy as np
import matplotlib.pyplot as plt

from streamlit_extras.let_it_rain import rain

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def preprocess_comment(comment):
    # Preprocess the comment by lowercasing and removing emojis
    comment = comment.lower()
    comment = re.sub(emoji.get_emoji_regexp(), '', comment)
    return comment

# Function to read and preprocess text
def preprocess_text(text):
    tokenizer = Tokenizer(num_words=MAX_WORDS)
    tokenizer.fit_on_texts([text])
    sequences = tokenizer.texts_to_sequences([text])
    input_sequence = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    return input_sequence

# Function to predict sentiment
def predict_sentiment(input_sequence):
    prediction = model.predict(input_sequence)
    predicted_class = np.argmax(prediction)
    if predicted_class == 0:
        predicted_sentiment = "Negative"
    else:
        predicted_sentiment = "Positive"
    return predicted_sentiment

# different YouTube URL formats
def extract_video_id(url):
    pattern = r"(?:(?:youtu\.be/|youtube\.com/(?:embed/|v/|watch\?v=|watch\?feature=player_embedded&v=))([^\?&\"'>]+))"
    
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    else:
        return None



lottie_animation = "https://lottie.host/0957557d-c660-463c-903c-86875b61db56/vpUomtC3Jr.json"

lottie_anim_jsom=load_lottieurl(lottie_animation)

st.write("""
         ## Welcome to Sentiment Analyser 😍😑☹️""")

st_lottie(lottie_anim_jsom,key="hello")

#for taking url
youtube_url = st.text_input("Enter a YouTube Video URL:")

if youtube_url:
    try:
        # Fetch video details using pytube
        video = YouTube(youtube_url)

        # Display video information
        st.subheader("Video Information:")
        st.write(f"Title: {video.title}")
        st.write(f"Author: {video.author}")
        st.write(f"Views: {video.views}")
        st.write(f"Published Date: {video.publish_date}")
        st.write(f"Description: {video.description}")

        # You can add more analysis or processing here
        # video_id = youtube_url.split("si=")[1]
        video_id = extract_video_id(youtube_url)
        st.write(f"Video id: {video_id}")

        api_key = ""
        youtube_service = build("youtube", "v3", developerKey=api_key)

        try:
            all_comments = []

            # maximum number of comments to display on the web app
            max_comments_to_display = 20
            max_comments_per_page = 100  # Maximum allowed by YouTube API

            # Retrieve comments using pagination
            page_token = None
            while True:
                results = youtube_service.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    textFormat="plainText",
                    maxResults=max_comments_per_page,
                    pageToken=page_token
                ).execute()

                # Extract comments from the current page
                comments = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in results["items"]]
                all_comments.extend(comments)

                # Check if there are more pages of comments
                if "nextPageToken" in results:
                    page_token = results["nextPageToken"]
                else:
                    break


            # Display a limited number of comments on the web app
            st.write("")
            st.subheader("Comments (Limited to Display):")
            for comment in all_comments[:max_comments_to_display]:
                st.write(comment)

            # Save all comments to a CSV file
            if all_comments:
                df = pd.DataFrame(all_comments, columns=["Comment"])
                df.to_csv("youtube_comments.csv", index=False)
                st.success("All comments saved to 'youtube_comments.csv'")
                Csv_to_text.csv_totxt()

                              

        except Exception as e:
            st.error("Error: Unable to retrieve comments. Please check the URL and your API key.")

    except Exception as e:
        st.error("Error: Unable to fetch video details. Please check the URL.")

# Load the trained model
if youtube_url:

    model = load_model(r'm1.hdf5')
    MAX_WORDS = 10000
    MAX_SEQUENCE_LENGTH = 1000

    # input_directory = r'C:\Users\Nandini\Documents\nanu\Youtube Comment Analysis\t'
    input_directory = os.getcwd().join("t");

    positive_count = 0
    negative_count = 0

    # Loop through each sentiment subdirectory

    sentiment_directory = os.path.join(input_directory)
        
        # Loop through each text file in the subdirectory
    with st.spinner('Processing...'):
        for file_name in os.listdir(sentiment_directory):
            file_path = os.path.join(sentiment_directory, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                input_sequence = preprocess_text(text)
                predicted_sentiment = predict_sentiment(input_sequence)
                if predicted_sentiment == "Positive":
                    positive_count += 1
                else:
                    negative_count += 1

    total_sentiments = positive_count + negative_count
    # positive_count,negative_count=negative_count,positive_count
    positive_to_negative_ratio = positive_count / negative_count



    st.subheader(f"Total positive sentiments: {positive_count}")
    st.subheader(f"Total negative sentiments: {negative_count}")
    st.subheader(f"Positive to Negative Ratio: {positive_to_negative_ratio}")

    st.write("")
    st.write("")
    st.write("## Graphical Representation")
    # Create a dictionary with sentiment labels and counts
    sentiment_labels = ["Positive", "Negative"]
    sentiment_counts = [positive_count, negative_count]
    custom_colors = ["#FFA500", "#B7C3F3"]

    fig, ax = plt.subplots()
    ax.pie(sentiment_counts, labels=sentiment_labels, autopct='%1.1f%%', startangle=90,colors=custom_colors,textprops={'color': 'white'})
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Set the background color of the plot to be transparent
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    st.pyplot(fig)

    if positive_count>negative_count:
        rain(
            emoji="😍",
            font_size=54,
            falling_speed=5,
            animation_length="infinite",
        )
    else:
        rain(
            emoji="😣",
            font_size=54,
            falling_speed=5,
            animation_length="infinite",
        )


# st.write("""
#             ### Made By Nandini💖""")        


    
