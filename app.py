import streamlit as st
import preprocessor
import core
def sorting(numb):
    if(numb.isalpha()):
        return(ord(numb[0]),numb)
    else:
        return(ord(numb[0])+100,numb)
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_files = st.sidebar.file_uploader("Choose a CSV file")
if uploaded_files is not None:
    bytes_data=uploaded_files.getvalue()
    data=bytes_data.decode("utf-8")
    df= preprocessor.preprocess(data)
    st.dataframe(df)
    user_list=list(df["User"].unique())
    user_list.remove("group notification")
    user_list=[x.capitalize() for x in user_list]
    user_list.sort(key=sorting)
    user_list.insert(0, "Overall")
    name=st.sidebar.selectbox("Select the user",user_list)
    name=name.capitalize()
    for i in range(len(df["User"])):
        df["User"].iloc[i]=df["User"].iloc[i].capitalize()
    if st.sidebar.button("Analyze"):
        c1,c2,c3,c4=st.columns(4)
        with c1:
            st.header("Total number of messages")
            nom=core.no_of_msgs(name,df)
            st.title(nom)
        with c2:
            st.header("Total Word Count")
            now=core.no_of_words(name,df)
            st.title(now)
        with c3:
            st.header("Media count")
            nom=core.no_of_media(name,df)
            st.title(nom)
        with c4:
            st.header("Links Shared")
            nol=core.no_of_links(name,df)
            st.title(nol)
        if name=="Overall":
            c1,c2=st.columns(2)
            with c1:
                st.header("Busiest ones")
                core.graph(df)
            with c2:
                st.header("Chat contribution in %")
                core.busy_ppl(df)

        core.most_common(name,df)
        core.emoji_analysis(name,df)