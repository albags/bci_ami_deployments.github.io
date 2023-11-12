import folium
from PIL import Image 
import base64
from io import BytesIO
import pandas as pd
import branca



def popup_html(row):
    i = row
    ami_id=df['AMI ID'].iloc[i] 
    camera_id=df['Camera ID'].iloc[i]
    single_board_computer = df['Single-board computer'].iloc[i] 
    light_type = df['Light type'].iloc[i] 
    power = df['Power'].iloc[i]
    images_folder = df['images_folder'].iloc[i]

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
    <html>
        <head>
            <h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(ami_id) + """
        </head>

        <style>
            .img{
                transition: transform .2s;
                width:50px;
                height:50px;
                margin:0 auto;
                background-color: rgb(173, 173, 237);
                border-radius: 10px;
                border: 1px solid black;
            }
            .img:hover {
                color: #424242; 
                -webkit-transition: all .3s ease-in;
                -moz-transition: all .3s ease-in;
                -ms-transition: all .3s ease-in;
                -o-transition: all .3s ease-in;
                transition: all .3s ease-in;
                opacity: 1;
                transform: scale(10);
                -ms-transform: scale(10); /* IE 9 */
                -webkit-transform: scale(10); /* Safari and Chrome */

            }
        </style>
        <table style="height: 126px; width: 350px;">
            <tbody>
                <tr>
                    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Camera ID</span></td>
                    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(camera_id) + """
                </tr>
                <tr>
                    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Single-board computer</span></td>
                    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(single_board_computer) + """
                </tr>
                <tr>
                    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Light type</span></td>
                    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(light_type) + """
                </tr>
                <tr>
                    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Power supply</span></td>
                    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(power) + """
                </tr>
                <tr>
                    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Deployment images</span></td>
                    <td style="width: 150px;background-color: """+ right_col_color +""";">
                        <img src="./images/{}/deployment/image1.jpg" class="img" alt="AMI system" width="10%" height="10%">
                    </td>""".format(images_folder) + """
                </tr>
            </tbody>
        </table>

    </html>
    """
    return html


df = pd.read_csv(r'./bci_ami_deployments.csv')
#Specify the center of the map by using the average of latitude and longitude coordinates
location = df['Latitude'].mean(), df['Longitude'].mean() 

# https://leaflet-extras.github.io/leaflet-providers/preview/
attr = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
)
tiles = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'

# Create a map centered around Panama
map_panama = folium.Map(location=location, zoom_start=14, tiles=tiles, attr=attr) #location=[9.15, -79.85]

# for point in points:
for i in range(0, len(df)):
    # labels=df['AMI ID'].iloc[i] #Create a lable that is the name of the institution
    html = popup_html(i)
    iframe = branca.element.IFrame(html=html,width=510,height=280)
    popup = folium.Popup(folium.Html(html, script=True), max_width=500)
    # https://www.flaticon.com/search?word=moth
    icon = folium.features.CustomIcon(icon_image=r'./images/moth_icon.png' , icon_size=(35,35))
    folium.Marker(
        location=[df['Latitude'].iloc[i],df['Longitude'].iloc[i]],
        tooltip="Click me!",
        icon=icon, 
        popup=popup
    ).add_to(map_panama)

# Load GeoJSON data after adding the markers
geojson_url = 'https://github.com/glynnbird/countriesgeojson/blob/master/panama.geojson'
panama_geojson = folium.GeoJson(geojson_url)
panama_geojson.add_to(map_panama)

# Save the map as an HTML file
map_panama.save('index.html')



