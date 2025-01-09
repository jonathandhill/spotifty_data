import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import io
import gzip

st.title('Spotify Dataset Analysis')

df = pd.read_csv('spotify_dataset.csv')
st.write(df.head())

english_songs = df[df['language'] == 'English']
non_eng = df[df['language'] != 'English']



songs_by_language = df['language'].value_counts()
songs_by_language.plot(kind="bar", title="Songs by Language")
plt.xlabel("Language")
plt.ylabel("Number of Songs")
st.pyplot(plt)
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

