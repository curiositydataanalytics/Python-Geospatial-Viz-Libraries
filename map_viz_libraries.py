# Data manipulation
import numpy as np
import datetime as dt
import pandas as pd
import geopandas as gpd

# Database and file handling
import os

# Data visualization
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import st_folium, folium_static
import seaborn as sns
import matplotlib.pyplot as plt
import graphviz
import pydeck as pdk
import folium
import leafmap.foliumap as leafmap
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
from shapely.geometry import Point, Polygon


path_cda = '\CuriosityDataAnalytics'
path_wd = path_cda + '\\wd'
path_data = path_wd + '\\data'

# App config
#----------------------------------------------------------------------------------------------------------------------------------#
# Page config
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)



# App title
st.title("Geospatial Visualization Libraries")
st.divider()

with st.sidebar:
    st.image(path_cda + '\\logo.png')

#
#

# 1)
#---------------------------------------------------------------------------------------#
st.header(':one: Initial map set-up')

cols = st.columns(4)
cols[0].subheader('Folium')
cols[0].code('''
import folium

m = folium.Map(location=[37.75644, -122.43825],
               zoom_start=11)

# Display in Streamlit
from streamlit_folium import folium_static
folium_static(m)


                    

#
''',
wrap_lines=True)

m = folium.Map(location=[37.75644, -122.43825], zoom_start=11)

with cols[0].expander('_'):
    folium_static(m, height=500, width=515)


#######################


cols[1].subheader('Leafmap')
cols[1].code('''
import leafmap.foliumap as leafmap

m = leafmap.Map(center=[37.75644, -122.43825],
                zoom=11)

# Display in Streamlit
m.to_streamlit()


             


#
''',
wrap_lines=True)

m = leafmap.Map(center=[37.75644, -122.43825], zoom=11)


with cols[1].expander('_'):
    m.to_streamlit(height=500, width=515)

#######################

cols[2].subheader('PyDeck')
cols[2].code('''
import pydeck as pdk

view_state = pdk.ViewState(longitude=-122.43825,
                           latitude=37.75644,
                           zoom=11)
             
m = pdk.Deck(initial_view_state=view_state)
             
# Display in Streamlit
st.pydeck_chart(m)

                       
#          
''',
wrap_lines=True)

m = pdk.Deck(initial_view_state=pdk.ViewState(longitude=-122.43825, latitude=37.75644, zoom=11), height=500)

with cols[2].expander('_'):
    st.pydeck_chart(m)

#######################


cols[3].subheader('Kepler.gl')
cols[3].code('''
from keplergl import KeplerGl

config = {"config":
             {"mapState":
                    {"latitude": 37.75644,
                     "longitude": -122.43825,
                     "zoom": 11}}}
             
m = KeplerGl(config=config)
             
# Display in Streamlit
from streamlit_keplergl import keplergl_static
keplergl_static(m)
''',
wrap_lines=True)

config = {"config": {"mapState": {"latitude": 37.75644, "longitude": -122.43825, "zoom": 11}}}

m = KeplerGl(height=500, config=config)

with cols[3].expander('_'):
    keplergl_static(m)

#######################




st.divider()

# 2)
#---------------------------------------------------------------------------------------#
st.header(':two: Map tiles ')

cols = st.columns(4)
cols[0].subheader('Folium')
cols[0].code('''
m = folium.Map(location=[37.75644, -122.43825],
               zoom_start=11,
               tiles="INSERT_TILE_NAME")


             
#
''',
wrap_lines=True)

with cols[0].expander('_'):
    subcols = st.columns(2)

    st.code('''tiles="CartoDB dark_matter"''')
    m = folium.Map(location=[37.75644, -122.43825], zoom_start=11, tiles='CartoDB dark_matter')
    folium_static(m, height=325, width=510)

    st.code('''tiles="OpenTopoMap"''')
    m = folium.Map(location=[37.75644, -122.43825], zoom_start=11, tiles='OpenTopoMap')
    folium_static(m, height=325, width=510)

    st.code('''tiles=folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri, USGS, NOAA',
        name='Esri World Imagery'
    )''')
    custom_tile = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri, USGS, NOAA',
        name='Esri World Imagery'
    )
    m = folium.Map(location=[37.75644, -122.43825], zoom_start=11, tiles=custom_tile)
    folium_static(m, height=325, width=510)

esri_tiles = folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri, USGS, NOAA',
    name='Esri World Imagery'
)
#######################

cols[1].subheader('Leafmap')
cols[1].code('''

m = leafmap.Map(center=[37.75644, -122.43825], zoom=11)
             
m.add_basemap('INSERT_TILE_NAME')

             

#
''')
with cols[1].expander('_'):
    st.code('''m.add_basemap('CartoDB.Positron')''')
    m = leafmap.Map(center=[37.75644, -122.43825], zoom=11)
    m.add_basemap('CartoDB.Positron')
    m.to_streamlit(height=325, width=515)

    st.code('''m.add_basemap('ROADMAP')''')
    m = leafmap.Map(center=[37.75644, -122.43825], zoom=11)
    m.add_basemap('ROADMAP')
    m.to_streamlit(height=325, width=515)

    st.code('''
m.add_tile_layer(
    url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    name='ESRI World Imagery',
    attribution='Esri, USGS, NOAA'
)''')
    m = leafmap.Map(center=[37.75644, -122.43825], zoom=11)
    custom_tile = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    m.add_tile_layer(
        url=custom_tile,
        name='ESRI World Imagery',
        attribution='Esri, USGS, NOAA'
    )
    m.to_streamlit(height=325, width=515)

#######################

cols[2].subheader('PyDeck')

cols[2].code('''
view_state = pdk.ViewState(longitude=-122.43825,
                           latitude=37.75644,
                           zoom=11)

m = pdk.Deck(initial_view_state=view_state,
             map_provider="INSERT_TILE_NAME",
             map_style="INSERT_MAP_STYLE")
''')

with cols[2].expander('_'):
    st.code('''
map_provider="carto"
map_style="light"
''')
    m = pdk.Deck(initial_view_state=pdk.ViewState(longitude=-122.43825, latitude=37.75644, zoom=11), height=325, map_provider="carto", map_style="light")
    st.pydeck_chart(m, use_container_width=True)

    st.code('''
map_provider="mapbox"
map_style="dark"
''')
    m = pdk.Deck(initial_view_state=pdk.ViewState(longitude=-122.43825, latitude=37.75644, zoom=11), height=325, map_provider="mapbox", map_style="dark")
    st.pydeck_chart(m, use_container_width=True)

    st.code('''
custom_layer = pdk.Layer(type="TileLayer",
                         get_tile_url="https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png",
)
m = pdk.Deck(layers=[custom_layer], ...)
''')
    custom_layer = pdk.Layer(type="TileLayer",
                             get_tile_url="https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png",
    )
    m = pdk.Deck(layers=[custom_layer], initial_view_state=pdk.ViewState(longitude=-122.43825, latitude=37.75644, zoom=11), height=325, map_style='mapbox://styles/mapbox/satellite-v9')
    st.pydeck_chart(m, use_container_width=True)

#######################

cols[3].subheader('Kepler.gl')
cols[3].code('''
m = KeplerGl()





#
''')

with cols[3].expander('_'):
    m = KeplerGl(height=325)
    keplergl_static(m)

st.divider()

# 3)
#---------------------------------------------------------------------------------------#
st.header(':three: Add Layers')

st.code('''
    pts = gpd.GeoDataFrame({
        'id' : ['A', 'B'],
        'geometry' : [Point(-122.4313, 37.7569),
                      Point(-122.4512, 37.7797)]
    }, crs=4326)

    poly = gpd.GeoDataFrame({
        'id': ['A'],
        'geometry': [Polygon([
            (-122.4251, 37.8013), (-122.4728, 37.7853),
            (-122.4227, 37.7493), (-122.4251, 37.8013)
        ])]
    }, crs=4326)
''')

pts = gpd.GeoDataFrame({
    'id' : ['A', 'B'],
    'geometry' : [Point(-122.4313, 37.7569),
                    Point(-122.4512, 37.7797)]
}, crs=4326)

poly = gpd.GeoDataFrame({
    'id': ['A'],
    'geometry': [Polygon([
        (-122.4251, 37.8013), (-122.4728, 37.7853),
        (-122.4227, 37.7493), (-122.4251, 37.8013)
    ])]
}, crs=4326)

cols = st.columns(4)
cols[0].subheader('Folium')

cols[0].code('''
    m = folium.Map(location=[37.75644, -122.43825])

    folium.GeoJson(pts).add_to(m)
    folium.GeoJson(poly).add_to(m)


             

             


             

             
#
''')

with cols[0].expander('_'):
    m = folium.Map(location=[37.75644, -122.43825], zoom_start=11, tiles='CartoDB positron')

    folium.GeoJson(pts).add_to(m)
    folium.GeoJson(poly).add_to(m)

    folium_static(m, height=325, width=510)

#######################

cols[1].subheader('Leafmap')

cols[1].code('''
m = leafmap.Map(center=[37.75644, -122.43825])
             
m.add_gdf(pts, layer_name="pts")
m.add_gdf(poly, layer_name="poly")



             
             




             
#
''')

with cols[1].expander('_'):
    m = leafmap.Map(center=[37.75644, -122.43825], zoom=12)
    m.add_basemap('CartoDB.Positron')
    m.add_gdf(pts, layer_name="pts")
    m.add_gdf(poly, layer_name="poly")
    m.to_streamlit(height=325, width=515)

#######################

cols[2].subheader('PyDeck')
cols[2].code('''
layers=[pdk.Layer(
            'ScatterplotLayer',
            data=pts,
            get_position='geometry.coordinates',
            get_radius=200
        ),
        pdk.Layer(
            'GeoJsonLayer',
            data=poly,
            get_fill_color=[0, 0, 255, 80]
        )
]
m = pdk.Deck(layers=layers,
             initial_view_state=pdk.ViewState(longitude=-122.43825, latitude=37.75644))
#''')
with cols[2].expander('_'):

    m = pdk.Deck(layers=[pdk.Layer(
                            'ScatterplotLayer',
                            data=pts,
                            get_position='geometry.coordinates',
                            get_radius=200
                        ),
                        pdk.Layer(
                            'GeoJsonLayer',
                            data=poly,
                            get_fill_color=[0, 0, 255, 80]
                        )],
                initial_view_state=pdk.ViewState(longitude=-122.43825, latitude=37.75644, zoom=11), height=325, map_provider="carto", map_style="light")
    st.pydeck_chart(m, use_container_width=True)


#######################

cols[3].subheader('Kepler.gl')

cols[3].code('''
m = KeplerGl()
             
m.add_data(data=pts, name='pts')
m.add_data(data=poly, name='poly')
             



             


             


#
''')

with cols[3].expander('_'):
    m = KeplerGl(height=325)
    m.add_data(data=pts, name='pts')
    m.add_data(data=poly, name='poly')
    keplergl_static(m)

st.divider()

# 4)
#---------------------------------------------------------------------------------------#
st.header(':four: Interactive Elements')
cols = st.columns(4)
cols[0].subheader('Folium')

cols[0].code('''
    folium.LayerControl().add_to(m)
    folium.plugins.Fullscreen().add_to(m)
    folium.plugins.MeasureControl().add_to(m)
    folium.plugins.MousePosition().add_to(m)
    folium.plugins.Search(m_pts, 'id').add_to(m)
    folium.plugins.MiniMap().add_to(m)





             


#
''')

with cols[0].expander('_'):
    m = folium.Map(location=[37.75644, -122.43825], zoom_start=11, tiles='CartoDB positron')

    m_pts = folium.GeoJson(pts, name='pts', tooltip=folium.GeoJsonTooltip(fields=['id'])).add_to(m)
    m_poly = folium.GeoJson(poly, name='poly').add_to(m)

    folium.LayerControl().add_to(m)
    folium.plugins.Fullscreen().add_to(m)
    folium.plugins.MeasureControl().add_to(m)
    folium.plugins.MousePosition().add_to(m)
    folium.plugins.Search(m_pts, 'id').add_to(m)

    folium.plugins.MiniMap('CartoDB positron').add_to(m)

    folium_static(m, height=325, width=510)

#######################

cols[1].subheader('Leafmap')

cols[1].code('''
#

            


             







             
#
''')

with cols[1].expander('_'):
    m = leafmap.Map(center=[37.75644, -122.43825], zoom=12)
    m.add_basemap('CartoDB.Positron')
    m.add_gdf(pts, layer_name="pts")
    m.add_gdf(poly, layer_name="poly")

    m.to_streamlit(height=325, width=515)

#######################

cols[2].subheader('PyDeck')
cols[2].code('''
layers=[pdk.Layer(
            'ScatterplotLayer',
            data=pts,
            get_position='geometry.coordinates',
            get_radius=200
        ),
        pdk.Layer(
            'GeoJsonLayer',
            data=poly,
            get_fill_color=[0, 0, 255, 80]
        )
]
m = pdk.Deck(layers=layers,
             initial_view_state=pdk.ViewState(longitude=-122.43825, latitude=37.75644))
#
''')
with cols[2].expander('_'):

    m = pdk.Deck(layers=[pdk.Layer(
                            'ScatterplotLayer',
                            data=pts,
                            get_position='geometry.coordinates',
                            get_radius=200
                        ),
                        pdk.Layer(
                            'GeoJsonLayer',
                            data=poly,
                            get_fill_color=[0, 0, 255, 80]
                        )],
                initial_view_state=pdk.ViewState(longitude=-122.43825, latitude=37.75644, zoom=11), height=325, map_provider="carto", map_style="light")
    st.pydeck_chart(m, use_container_width=True)

#######################

cols[3].subheader('Kepler.gl')

cols[3].code('''
#





             







#
''')

with cols[3].expander('_'):
    m = KeplerGl(height=325)
    m.add_data(data=pts, name='pts')
    m.add_data(data=poly, name='poly')
    keplergl_static(m)

st.divider()

# 5)
#---------------------------------------------------------------------------------------#
st.header(':five: Cloropleth ')

st.code('''
poly = gpd.read_file('geo_export_c7e6d58b-b43e-48a9-a7b8-5fbc0e0a039b.shp')


''')

poly = gpd.read_file(path_data + '\\cbg_sf.shp')
np.random.seed(42)
poly['metric'] = np.random.normal(loc=0, scale=1, size=len(poly))

with st.expander('geometry'):
    st.dataframe(poly[['geometry', 'metric']])

cols = st.columns(4)
cols[0].subheader('Folium')

cols[0].code('''
    m = folium.Map(location=[37.75644, -122.43825])

    folium.Choropleth(geo_data=poly,
                      data=poly,
                      columns=['geoid', 'metric'],
                      key_on='feature.properties.geoid',
                      fill_color='YlGn').add_to(m)            
#
''')

with cols[0].expander('_'):
    m = folium.Map(location=[37.75644, -122.43825], zoom_start=11, tiles='CartoDB positron')

    folium.Choropleth(geo_data=poly, data=poly, columns=['geoid', 'metric'], key_on='feature.properties.geoid', fill_color='YlGn').add_to(m)

    folium_static(m, height=325, width=510)

####################### 
 
cols[1].subheader('Leafmap')

cols[1].code('''
m = leafmap.Map(center=[37.75644, -122.43825])
             
m.add_data(poly,
           layer_name="poly",
           column='metric',
           cmap='YlGn')
                        
#
''')

with cols[1].expander('_'):
    m = leafmap.Map(center=[37.75644, -122.43825], zoom=11)
    m.add_basemap('CartoDB.Positron')
    m.add_data(poly, layer_name="poly", column='metric', cmap='YlGn')
    m.to_streamlit(height=325, width=515)

#######################



import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
cmap = plt.get_cmap('YlGn')
norm = mcolors.Normalize(vmin=poly['metric'].min(), vmax=poly['metric'].max())
def get_color(metric_value):
    rgba = cmap(norm(metric_value))
    return [int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255), 255]
poly['color'] = poly['metric'].apply(get_color)

cols[2].subheader('PyDeck')
cols[2].code('''
layers=[pdk.Layer(
            'GeoJsonLayer',
            data=poly,
            get_fill_color='color'
        )
]
m = pdk.Deck(layers=layers,
             initial_view_state=pdk.ViewState(longitude=-122.43825, latitude=37.75644))
''')
with cols[2].expander('_'):

    m = pdk.Deck(layers=[pdk.Layer(
                            'GeoJsonLayer',
                            data=poly,
                            get_fill_color='color'
                        )],
                initial_view_state=pdk.ViewState(longitude=-122.43825, latitude=37.75644, zoom=11), height=325, map_provider="carto", map_style="light")
    st.pydeck_chart(m, use_container_width=True)


#######################

cols[3].subheader('Kepler.gl')

cols[3].code('''
m = KeplerGl()
             
m.add_data(data=pts, name='pts')
m.add_data(data=poly, name='poly')
             


#
''')

with cols[3].expander('_'):
    m = KeplerGl(height=325)
    m.add_data(data=poly, name='poly')
    keplergl_static(m)

st.divider()


# 6)
#---------------------------------------------------------------------------------------#
st.header(':six: Heatmap')

st.code('''
poly = gpd.read_file('geo_export_c7e6d58b-b43e-48a9-a7b8-5fbc0e0a039b.shp')
''')

poly = gpd.read_file(path_data + '\\cbg_sf.shp')
np.random.seed(42)
poly = gpd.GeoDataFrame(poly, geometry=gpd.points_from_xy(x=poly.intptlat, y=poly.intptlon, crs=4326), crs=4326)
poly['weight'] = np.random.randint(1, 1001, size=len(poly))
poly['lat'] = poly.geometry.x
poly['lon'] = poly.geometry.y

with st.expander('geometry'):
    st.dataframe(poly[['geometry', 'weight']])

cols = st.columns(4)
cols[0].subheader('Folium')

cols[0].code('''
    m = folium.Map(location=[37.75644, -122.43825])

    poly_heat = [[point.y, point.x, weight] for point, weight in zip(poly.geometry, poly['weight'])]

    folium.plugins.HeatMap(poly_heat).add_to(m)

        
#
''',
wrap_lines=True)

with cols[0].expander('_'):
    m = folium.Map(location=[37.75644, -122.43825], zoom_start=11, tiles='CartoDB positron')

    poly_heat = [[point.y, point.x, weight] for point, weight in zip(poly.geometry, poly['weight'])]

    folium.plugins.HeatMap(poly_heat).add_to(m)

    folium_static(m, height=325, width=510)

####################### 
 
cols[1].subheader('Leafmap')

cols[1].code('''
m = leafmap.Map(center=[37.75644, -122.43825])
             
m.add_heatmap(poly,
             latitude='lat',
             longitude='lon',
             value='weight')

                        
#
''')

with cols[1].expander('_'):
    m = leafmap.Map(center=[37.75644, -122.43825], zoom=11)
    m.add_basemap('CartoDB.Positron')
    m.add_heatmap(poly, latitude='lat', longitude='lon', value='weight', radius=10, blur=15)
    m.to_streamlit(height=325, width=515)

#######################

cols[2].subheader('PyDeck')
cols[2].code('''
layers=[pdk.Layer(
                "HeatmapLayer",
                data=poly,
                get_position=["lon", "lat"],
                get_weight="weight"
            )
]
m = pdk.Deck(layers=layers,
             initial_view_state=pdk.ViewState(longitude=-122.43825, latitude=37.75644))
''')
with cols[2].expander('_'):

    m = pdk.Deck(layers=[pdk.Layer(
                            "HeatmapLayer",
                            data=poly,
                            get_position=["lon", "lat"],
                            get_weight="weight",
                            radius_pixels=20,
                            intensity=1,
                            threshold=0.3,
                            max_zoom=16
                        )],
                initial_view_state=pdk.ViewState(longitude=-122.43825, latitude=37.75644, zoom=11), height=325, map_provider="carto", map_style="light")
    st.pydeck_chart(m, use_container_width=True)

m.to_html(path_data + '\\my_pydeck_map.html')
#######################

cols[3].subheader('Kepler.gl')

cols[3].code('''
m = KeplerGl()
             

             

           


#
''')

with cols[3].expander('_'):
    m = KeplerGl(height=326)
    m.add_data(data=poly, name='poly')
    keplergl_static(m)

st.divider()

# 7)
#---------------------------------------------------------------------------------------#
st.header(':seven: Exporting')

import webbrowser

cols = st.columns(4)
cols[0].subheader('Folium')
cols[0].code('''
m.save('my_folium_map.html')
''',
wrap_lines=True)

if cols[0].button('my_folium_map.html'):
    file_path = os.path.expanduser(path_data + '\\my_folium_map.html')
    webbrowser.open_new_tab(f'file://{file_path}')

#######################


cols[1].subheader('Leafmap')
cols[1].code('''
m.to_html('my_leafmap_map.html')
''',
wrap_lines=True)

m = leafmap.Map(center=[37.75644, -122.43825], zoom=11)

if cols[1].button('my_leafmap_map.html'):
    file_path = os.path.expanduser(path_data + '\\my_leafmap_map.html')
    webbrowser.open_new_tab(f'file://{file_path}')

#######################

cols[2].subheader('PyDeck')
cols[2].code('''
m.to_html('my_pydeck_map.html')       
''',
wrap_lines=True)

if cols[2].button('my_pydeck_map.html'):
    file_path = os.path.expanduser(path_data + '\\my_pydeck_map.html')
    webbrowser.open_new_tab(f'file://{file_path}')

#######################


cols[3].subheader('Kepler.gl')
cols[3].code('''
m.save_to_html(file_name='my_keplergl_map.html')
''',
wrap_lines=True)

if cols[3].button('my_keplergl_map.html'):
    file_path = os.path.expanduser(path_data + '\\my_keplergl_map.html')
    webbrowser.open_new_tab(f'file://{file_path}')

#######################

st.divider()

