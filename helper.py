from urlextract import URLExtract as extract
# from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = extract()


def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    num_message = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch no. of media messages
    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_message, len(words), num_media_msg, len(links)


def fetch_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


# def create_wordcloud(selected_user, df):
#     if selected_user != "Overall":
#         df = df[df['user'] == selected_user]
#
#     wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
#     df_wc = wc.generate(df['message'].str.cat(sep=" "))
#     return df_wc

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'Group Notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df


def emojis_top(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.distinct_emoji_list(c)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df
