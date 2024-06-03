#pydeck test

import time
import pydeck as pdk
import pandas as pd

df = pd.read_csv('test.csv')

def format_column(column):
    print("column:", column)
    column = column.replace('‘', '').replace('’', '').strip("[]")
    print("column-new:", column.split(','))

    for brands in column.split(','):
        print("brands", brands)
    #  brand_list = [{'name': brand} for brands in column for brand in brands]
    # return {'brand': brand_list, 'num': len(brand_list)}
    return {'brand': [{'name': brands} for brands in column.split(',')], 'num': len(column.split(','))}

# Convert the DataFrame into the desired format
formatted_data = {}
for column in df.columns:  # df.iloc[:,:-3].columns
    print(column)
    if (column == 'latitude' or column == 'longitude' or column == 'rank'):
        formatted_data[column] = df[column]
    else :
        formatted_data[column] = df[column].apply(format_column)

# Create a new DataFrame from the formatted data
formatted_df = pd.DataFrame(formatted_data)

# Display the new DataFrame
print(formatted_df)


# print(df)
Color = [
  [1, 152, 189],
  [73, 227, 206],
  [216, 254, 181],
  [254, 237, 177],
  [254, 173, 84],
  [209, 55, 78]
]

#bookingRef = df["bookingRef"]
#startHour = df["startHour"]
#endHour = df["endHour"]

layer = pdk.Layer(
    'HexagonLayer',
    data = formatted_df, 
    colorRange = Color,
    get_position=['longitude', 'latitude'],
	get_elevation_weight='MoT1',
    auto_highlight=True,
    elevation_scale=8000,
    filled=False,
    pickable=True,
    radius=500,
    elevation_range=[0, 10],
    extruded=True,
    controller = True,
    coverage=1)


#tooltip = {"html": "<b>Booking Reference:</b> {bookingRef} <br /><b>Start Hour:</b> {startHour}<br /><b>End Hour:</b> {endHour}"}
tooltip = {
   "html": "<b>Campaigns:</b> {elevationValue}",
   "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
}
# Set the viewport location
view_state = pdk.ViewState(
    longitude=-1.415,
    latitude=52.2323,
    zoom=6,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36)

# Combined all of it and render a viewport
r = pdk.Deck(layers=[layer], map_style="dark",initial_view_state=view_state,tooltip=tooltip)
r.to_html('hexagonsOther3.html')
