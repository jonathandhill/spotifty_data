import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide") #Wide mode

st.title('Spotify Dataset Analysis')

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

df = load_data('spotify_dataset.csv')
    
st.write(df.head())

english_songs = df[df['language'] == 'English'] 
non_eng = df[df['language'] != 'English']

@st.cache_data
def plot_songs_by_language(df):
    #Songs by Language
    df_sorted = df['language'].value_counts().sort_values().reset_index()
    df_sorted.columns = ['language', 'count']

    canv = plt.figure(figsize = (20,8), facecolor = 'white') #blank canvas with background
    grid = canv.add_gridspec(1,1) #grid layout
    subplot = canv.add_subplot(grid[0,0]) #subplot

    subplot.text(3.5, 28000, 
            'Songs by Language', 
            fontsize=25, 
            fontweight='bold', 
            fontfamily='monospace')

    #Dotted horizontal gridlines
    subplot.grid(color='black', linestyle=':', axis='y', zorder=0,  dashes=(1,5))

    sns.barplot(data=df_sorted, x ='language', y='count', ax = subplot, alpha = 1, zorder = 2)

    #Remove border lines
    for direction in ['top','right','left']:
        subplot.spines[direction].set_visible(False)

    subplot.set_xlabel('Language', fontsize = 14, fontweight = 'bold')
    subplot.tick_params(axis = 'x', labelsize=14)
    subplot.tick_params(axis = 'y', length=0, labelsize=13)
    subplot.set_ylabel('',)
    subplot.invert_xaxis()
    return canv

canv = plot_songs_by_language(df)
st.pyplot(canv)

# Tableau embed code
tableau_html = """
<div class='tableauPlaceholder' id='viz1736255076662' style='position: relative'>
    <noscript>
        <a href='#'>
            <img alt='Average Popularity Trends ' src='https://public.tableau.com/static/images/Sp/Spotify_17362545262740/AvPoptrends/1_rss.png' style='border: none' />
        </a>
    </noscript>
    <object class='tableauViz' style='display:none;'>
        <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
        <param name='embed_code_version' value='3' /> 
        <param name='site_root' value='' />
        <param name='name' value='Spotify_17362545262740/AvPoptrends' />
        <param name='tabs' value='no' />
        <param name='toolbar' value='yes' />
        <param name='static_image' value='https://public.tableau.com/static/images/Sp/Spotify_17362545262740/AvPoptrends/1.png' /> 
        <param name='animate_transition' value='yes' />
        <param name='display_static_image' value='yes' />
        <param name='display_spinner' value='yes' />
        <param name='display_overlay' value='yes' />
        <param name='display_count' value='yes' />
        <param name='language' value='en-GB' />
        <param name='filter' value='publish=yes' />
    </object>
</div>

<script type='text/javascript'>
    var divElement = document.getElementById('viz1736255076662');
    var vizElement = divElement.getElementsByTagName('object')[0];
    vizElement.style.width='100%';
    vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
    var scriptElement = document.createElement('script');
    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
    vizElement.parentNode.insertBefore(scriptElement, vizElement);
</script>
"""

# Embed the Tableau visualization
st.components.v1.html(tableau_html, height=900)

#Features line graph
audio_features = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']

colormap = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d']

audio_data = pd.DataFrame(df.groupby('year')[audio_features].mean().sort_index()).reset_index()

fig = plt.figure(figsize=(20, 8), facecolor='white')
gs = fig.add_gridspec(1, 1)
ax = fig.add_subplot(gs[0, 0])

ax.text(1970, 1.0, 
        'Year Wise Distribution of Audio Features', 
        fontsize=45, 
        fontweight='bold', 
        fontfamily='monospace')

#Initialise session state
if 'features_to_plot' not in st.session_state:
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
        st.session_state.features_to_plot[feature] = st.session_state[f'checkbox_{feature}']

if any(st.session_state.features_to_plot.values()):
    for feature, color in zip(audio_features, colormap):
        if st.session_state.features_to_plot[feature]:
            sns.lineplot(data=audio_data.iloc[1:, ], x='year', y=feature, color=color, label=feature, ax=ax)
    
    for direction in ['top','right','left']:
        ax.spines[direction].set_visible(False)
        
    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis = 'y', length=0)  
    ax.set_xlabel('Year', fontsize=15, fontweight='bold')
    ax.set_ylabel('')
    ax.legend(loc='upper right', fontsize=10)

    st.pyplot(plt)
else:
    st.info('Please select at least one feature to display the plot.')

col1, col2 = st.columns(2)
col1.button('Clear All', key='clear_btn', on_click=clear_all)
col2.button('Select All', key='select_btn', on_click=select_all)

# Create horizontal columns for checkboxes
num_features = len(audio_features)
cols = st.columns(num_features)  # Creates one column per feature

# Create checkboxes in horizontal layout
for idx, (feature, col) in enumerate(zip(audio_features, cols)):
    st.session_state.features_to_plot[feature] = col.checkbox(
        f'{feature.capitalize()}', 
        value=st.session_state.features_to_plot[feature],
        key=f'checkbox_{feature}', 
        on_change=update_feature_state
    )

@st.cache_data
def year_to_decade(year):
    decade = (year//10) * 10
    decade = f'{decade}s'
    return decade

df['decade'] = df['year'].apply(lambda x: year_to_decade(x))

@st.cache_data
def plot_songs_by_decade(df):
    fig = plt.figure(figsize = (20,8), facecolor = 'white') #blank canvas with background
    gs = fig.add_gridspec(1,1) #grid layout
    ax = fig.add_subplot(gs[0,0]) #subplot

    ax.text(3.5, 28000, 
            'Songs Released(By Decade)', 
            fontsize=25, 
            fontweight='bold', 
            fontfamily='monospace')

    #Dotted horizontal gridlines
    ax.grid(color='black', linestyle=':', axis='y', zorder=0,  dashes=(1,5))

    sns.countplot(data = df, x ='decade', ax = ax, alpha = 1, zorder = 2)

    #Remove border lines
    for direction in ['top','right','left']:
        ax.spines[direction].set_visible(False)

    ax.set_xlabel('Decade', fontsize = 14, fontweight = 'bold')
    ax.tick_params(axis = 'x', labelsize=14)
    ax.tick_params(axis = 'y', length=0, labelsize=13)
    ax.set_ylabel('',)
    ax.invert_xaxis()
    return fig

fig = plot_songs_by_decade(df)
st.pyplot(fig)