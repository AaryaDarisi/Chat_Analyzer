import streamlit as st
from urlextract import URLExtract
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import emoji

extract = URLExtract()


def no_of_msgs(name, df):
    if name == "Overall":
        return len(df["User"])
    return len(df[df["User"] == name])


def no_of_words(name, df):
    tot = 0
    if name == "Overall":
        for msg in df["Message"]:
            tot += len(msg.split(' '))
    else:
        for msg in df[df["User"] == name]["Message"]:
            tot += len(msg.split(' '))
    return tot


def no_of_media(name, df):
    tot = 0
    if name == "Overall":
        for msg in df["Message"]:
            if (msg == "<Media omitted>\n"):
                tot += 1
    else:
        for msg in df[df["User"] == name]["Message"]:
            if (msg == "<Media omitted>\n"):
                tot += 1
    return tot


def no_of_links(name, df):
    links = []
    if name == "Overall":
        for msg in df["Message"]:
            links.extend(extract.find_urls(msg))
    else:
        for msg in df[df["User"] == name]["Message"]:
            links.extend(extract.find_urls(msg))
    return len(links)


def busy_ppl(df):
    st.dataframe(round((df["User"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"count": "% contributed"}))


def graph(df):
    x = df["User"].value_counts().head()
    names = x.index
    count = x.values
    fig, ax = plt.subplots()
    ax.bar(names, count)
    plt.xticks(rotation="vertical")
    st.pyplot(fig)


def most_common(name,df):
    file = open('stopwords.txt', 'r')
    stopwords = file.read()
    if(name!="Overall"):
        df=df[df["User"]==name]
    new_df = df[df["User"] != "group notification"]
    new_df = new_df[new_df["Message"] != "<Media omitted>\n"]
    new_df = new_df[new_df["Message"] != "This message was deleted\n"]
    words = []
    for msg in new_df["Message"]:
        for msg2 in msg.lower().split(' '):
            if msg2 not in stopwords:
                words.append(msg2)
    common_df = pd.DataFrame(Counter(words).most_common(20))
    common_df=common_df.rename(columns={0: "word", 1: "count"})

    fig,ax=plt.subplots()
    ax.bar(common_df["word"],common_df["count"])
    plt.xticks(rotation="vertical")
    st.header("MOST USED WORDS")
    c1,c2=st.columns(2)
    with c1:
        st.pyplot(fig)
    with c2:
        st.dataframe(common_df)


def emoji_analysis(name,df):
    if (name != "Overall"):
        df = df[df["User"] == name]
    emojis=[]
    for msg in df["Message"]:
        for msg2 in msg:
            if msg2 in emoji.UNICODE_EMOJI['en']:
                emojis.extend(msg2)
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    # st.dataframe(emoji_df)
    st.write("Emoji Analysis")
    c1,c2=st.columns(2)
    with c1:
        fig,ax=plt.subplots()
        ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
        st.pyplot(fig)
    with c2:
        st.dataframe(emoji_df)