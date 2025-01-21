import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")  # Wide mode

st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
    }
    .centered-header {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

df = load_data("spotify_dataset.csv")

english_songs = df[df["language"] == "English"]
non_eng = df[df["language"] != "English"]

time_sig_one = len(df[df['time_signature'] == 1.0])

st.markdown('<h1 class="centered-title">Spotify Dataset Analysis</h1>', unsafe_allow_html=True)
st.markdown('<div style="display: flex; flex-wrap: wrap; gap: 4px; justify-content: center;"><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" height="32" alt="Python" style="margin-right: 4px"><img src="https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas" height="32" alt="Pandas" style="margin-right: 4px"><img src="https://img.shields.io/badge/-Matplotlib-000000?style=flat&logo=python" height="32" alt="Matplotlib" style="margin-right: 4px"><img src="https://img.shields.io/static/v1?label=Powered%20by&message=seaborn&color=E523F5&style=flat" height="32" alt="Seaborn" style="margin-right: 4px"><img src="https://img.shields.io/badge/Jupyter-notebook-brightgreen" height="32" alt="Jupyter" style="margin-right: 4px"><img src="https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=Tableau&logoColor=white" height="32" alt="Tableau" style="margin-right: 4px"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="centered-header">Jonathan Hill</h2>', unsafe_allow_html=True)
st.markdown('<p align="center"><a href="https://www.linkedin.com/in/jonathanburthill/" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" height="28" style="margin-right: 4px"></a> <a href="https://github.com/jonathandhill" target="_blank"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" height="28" style="margin-right: 4px"></a> <a href="mailto:jonathan.burt.hill@gmail.com" aria-label="Send an email to Jonathan Hill"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" height="28" style="margin-right: 4px"></a></p>', unsafe_allow_html=True)
with st.expander('See business case & general data issues'):
    st.write('### Business Case')
    st.write('This project investigates how popular music has evolved over time through analysis of Spotify\'s audio feature data. Using metrics such as acousticness, danceability, energy, tempo, and valence, we\'ll examine trends in musical characteristics across different time periods. The analysis will focus on quantifying and visualizing changes in these musical attributes to understand how production styles and preferences have shifted. Our goal is to uncover meaningful patterns in how music has transformed, potentially revealing insights about changing cultural tastes and production techniques.')
    st.write('### General Data Issues')
    st.write('*Time Signature:*')
    st.write('- Incorrect values (e.g. Maroon 5 songs *Cold* has 0.0 value, *Nobody’s Love - Remix* has 1.0 value. *Not Afraid* by Eminem has 5.0 value)')
    st.write(f'- {time_sig_one} songs with value of 1.0')

st.divider()


st.sidebar.write('### Statistics')
total_songs = len(df)
total_artists = df['artist_name'].nunique()
year_range = f"{df['year'].min()} and {df['year'].max()}"
most_songs_year = df['year'].value_counts().idxmax()
least_songs_year = df['year'].value_counts().idxmin()

st.sidebar.write(f'Total number of songs: {total_songs:,}')
st.sidebar.write(f'Total number of artists: {total_artists:,}')
st.sidebar.write(f'Between {year_range}')
st.sidebar.write(f'Most songs written in {most_songs_year}, least in {least_songs_year}')

st.sidebar.write('### Features')
st.sidebar.write('*Acousticness* - A confidence measure of whether the track is acoustic.')
st.sidebar.write('*Danceability* - How suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. ')
st.sidebar.write('*Energy* - Represents a perceptual measure of intensity and activity. Features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.')
st.sidebar.write('*Instrumentalness* - Predicts whether a track contains no vocals.')
st.sidebar.write('*Liveness* - Higher liveness values represent an increased probability that the track was performed live (with an audience).')
st.sidebar.write('*Valence* - The musical positiveness. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).')

top_prol_artists_col, shakar, pop_artists_col, big_dawgs = st.columns(4, vertical_alignment="center", border=False)

@st.cache_data
def get_top_prolific_artists(df):
    top_prol_artists = df['artist_name'].value_counts(sort=True).head()
    top_prol_artists = top_prol_artists.reset_index().rename(columns={'index': 'Artist', 'artist_name': 'Artist', 'count': 'Count'})
    top_prol_artists.index = top_prol_artists.index + 1
    return top_prol_artists

@st.cache_data
def year_to_decade(year):
    decade = (year // 10) * 10
    decade = f"{decade}s"
    return decade

df["decade"] = df["year"].apply(lambda x: year_to_decade(x))

@st.cache_data
def plot_songs_by_decade(df):
    fig = plt.figure(figsize=(20, 8), facecolor="white")  # blank canvas with background
    gs = fig.add_gridspec(1, 1)  # grid layout
    ax = fig.add_subplot(gs[0, 0])  # subplot

    ax.text(
        3.5,
        28000,
        "Songs Released(By Decade)",
        fontsize=25,
        fontweight="bold",
        fontfamily="monospace",
    )

    # Dotted horizontal gridlines
    ax.grid(color="black", linestyle=":", axis="y", zorder=0, dashes=(1, 5))

    sns.countplot(data=df, x="decade", ax=ax, alpha=1, zorder=2, color='skyblue')

    # Remove border lines
    for direction in ["top", "right", "left"]:
        ax.spines[direction].set_visible(False)

    ax.set_xlabel("Decade", fontsize=14, fontweight="bold")
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", length=0, labelsize=13)
    ax.set_ylabel(
        "",
    )
    ax.invert_xaxis()
    return fig

# Add a title
top_prol_artists_col.write("### Top 5 Most Prolific Artists")

# Display the table
top_prol_artists = get_top_prolific_artists(df)
top_prol_artists_col.table(top_prol_artists)


shakar.image('shankar_mahadevan.jpeg', width=250)

@st.cache_data
def get_top_popular_artists(df):
    pop_artists = df.sort_values('popularity', ascending=False).head().reset_index()
    pop_artists = pop_artists[['track_name', 'artist_name', 'popularity']]
    pop_artists.index = pop_artists.index + 1
    pop_artists = pop_artists.rename(columns={'index': 'Rank', 'track_name': 'Track', 'artist_name': 'Artist', 'popularity': 'Popularity'})
    pop_artists['Track'] = pop_artists['Track'].apply(lambda x: x.split(' - ')[0])
    return pop_artists

@st.cache_data
def plot_songs_by_language(df):
    #Only display percentage if percentage > 5%
    def autopct_func(pct):
        return ('%1.1f%%' % pct) if pct > 5 else ''
    # Songs by Language
    df_sorted_lang = df["language"].value_counts().sort_values().reset_index()
    df_sorted_lang.columns = ["language", "count"]
    
    palette_color = sns.color_palette('bright') 
    
    #Only display labels if percentage > 5%
    total_count = df_sorted_lang['count'].sum()
    labels = [
        f"{label}" if count / total_count > 0.05 else ''
        for label, count in zip(df_sorted_lang['language'], df_sorted_lang['count'])
    ]
    
    canv = plt.figure(figsize=(2.5, 2.5))
    plt.pie(
        df_sorted_lang['count'], 
        labels=labels, 
        colors=palette_color, 
        autopct=autopct_func,
        textprops={'fontsize': 5.5}
    )
    plt.title('Songs by Language', fontsize=10)
    plt.text(0, -1.2, 'Remaining slices: Telagu (5%) and Malayalam (5%)', ha='right', fontsize=4)
    plt.tight_layout() 
   
    return canv

pop_artists_col.write("### Top 5 Most Popular Artists")
pop_artists = get_top_popular_artists(df)
pop_artists_col.table(pop_artists)
big_dawgs.image('big_dawgs.jpeg', width=250)

songs_by_decade_col, language_pie_col = st.columns(2, vertical_alignment="center", border=True)

fig = plot_songs_by_decade(df)
songs_by_decade_col.pyplot(fig)

language_pie_chart = plot_songs_by_language(df)
language_pie_col.pyplot(language_pie_chart)

# Tableau embed code
tableau_html = """
<div class='tableauPlaceholder' id='viz1736934652251' style='position: relative'><noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Sp&#47;Spotify_17362545262740&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Spotify_17362545262740&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Sp&#47;Spotify_17362545262740&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1736934652251');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
"""
# Embed the Tableau visualization
st.components.v1.html(tableau_html, height=1400)

# Features line graph
audio_features = [
    "danceability",
    "energy",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
]

colormap = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e", "#e6ab02", "#a6761d"]

audio_data = pd.DataFrame(
    df.groupby("year")[audio_features].mean().sort_index()
).reset_index()

fig = plt.figure(figsize=(20, 8), facecolor="white")
gs = fig.add_gridspec(1, 1)
ax = fig.add_subplot(gs[0, 0])

ax.text(
    1973,
    0.9,
    "Year Wise Distribution of Audio Features",
    fontsize=40,
    fontweight="bold",
    fontfamily="monospace",
)

# Initialise session state
if "features_to_plot" not in st.session_state:
    st.session_state.features_to_plot = {feature: True for feature in audio_features}


# callback functions for the buttons
def clear_all():
    for feature in audio_features:
        st.session_state.features_to_plot[feature] = False


def select_all():
    for feature in audio_features:
        st.session_state.features_to_plot[feature] = True


def update_feature_state():
    # Update features_to_plot based on checkbox states
    for feature in audio_features:
        st.session_state.features_to_plot[feature] = st.session_state[
            f"checkbox_{feature}"
        ]


if any(st.session_state.features_to_plot.values()):
    for feature, color in zip(audio_features, colormap):
        if st.session_state.features_to_plot[feature]:
            sns.lineplot(
                data=audio_data.iloc[1:,],
                x="year",
                y=feature,
                color=color,
                label=feature,
                ax=ax,
            )

    for direction in ["top", "right", "left"]:
        ax.spines[direction].set_visible(False)

    ax.tick_params(axis="y", labelsize=14)
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Year", fontsize=13, fontweight="bold")
    ax.set_ylabel("Average value", fontsize=13, fontweight="bold")
    legend = ax.legend(loc="upper right", fontsize=10)

    # Change legend labels to uppercase
    for text in legend.get_texts():
        text.set_text(text.get_text().capitalize())

    st.pyplot(plt)
else:
    st.info("Please select at least one feature to display the plot.")

clear_col, select_col2 = st.columns(2)
clear_col.button("Clear All", key="clear_btn", on_click=clear_all)
select_col2.button("Select All", key="select_btn", on_click=select_all)

# horizontal columns for checkboxes
num_features = len(audio_features)
cols = st.columns(num_features)  # one column per feature

# Create checkboxes in horizontal layout
for idx, (feature, col) in enumerate(zip(audio_features, cols)):
    st.session_state.features_to_plot[feature] = col.checkbox(
        f"{feature.capitalize()}",
        value=st.session_state.features_to_plot[feature],
        key=f"checkbox_{feature}",
        on_change=update_feature_state,
    )

