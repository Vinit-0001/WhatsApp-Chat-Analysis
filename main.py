import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
# from wordcloud import WordCloud

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Chose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_msg, num_links = helper.fetch_stats(selected_user, df)
        col_1, col_2, col_3, col_4 = st.columns(4)

        with col_1:
            st.header("Total Messages")
            st.title(num_messages)
        with col_2:
            st.header("Total Words")
            st.title(words)
        with col_3:
            st.header("Media Shared")
            st.title(num_media_msg)
        with col_4:
            st.header("Links Shared")
            st.title(num_links)

        # finding the busiest user in the group
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, new_df = helper.fetch_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # # WordCloud
        # df_wc = helper.create_wordcloud(selected_user, df)
        # fig, ax = plt.subplots()
        # ax.imshow(df_wc)
        # st.title("WordCloud of Chats")
        # st.pyplot(fig)

        # most common words

        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation = "vertical")
        st.title("Most Common Words")
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji(selected_user,df)
        st.dataframe(emoji_df)