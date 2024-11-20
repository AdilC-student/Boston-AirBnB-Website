"""
Adil Chaudhry
Professor Frydenberg
CS-230-6
Final Project: Boston AirBnB Website
Program Description: This program creates a website using streamlit that explores Boston's
AirBnB market. This code utilizes different extensions such as pydeck for map visualization,
matplotlib for chart visualization with labeled axis', as well as pandas for data conversion.
The website that is created displays a variety of different information for someone whose searching the
Boston AirBnB market!
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import os

# Loading the AirBnB data (3 Data Sheets stored in Zip File,
def load_airbnb_data():
    file_path = os.path.join(os.path.dirname(__file__), 'Boston-AirBnb-Data-Folder', 'listings.csv')
    listings = pd.read_csv(file_path)
    return listings

# [PY2] A function that returns more than one value (Getting the Min & Max Price for AirBnB's)
def airbnb_price_statistics(data):
    min_price = data['price'].min()
    max_price = data['price'].max()
    return min_price, max_price

# Loading the data up
airbnb_data = load_airbnb_data()

# [DA1] Clean or manipulate data (cleaning data with lambda)
airbnb_data = airbnb_data.dropna(subset=['price', 'latitude', 'longitude', 'room_type'])

# [DA9] Perform calculations on DataFrame columns (going through the data)
airbnb_data['price_per_night'] = airbnb_data['price'] / airbnb_data['minimum_nights']

# Page title and description (Main Title & Main Description)
st.title("Welcome to Boston's AirBnB Market!")
st.write("Let's explore Boston's AirBnB Market with our interactive map and insightful visualizations. "
         "You can filter the different listings by neighborhood and price range on the left-hand side of the website. "
         "This will help you gain a better insight into the vast AirBnB Market here in Boston.")

# Streamlit Controls (Sidebar Controls)
st.sidebar.header("Filter Criteria")


# [ST1] Dropdown widget (Dropdown Widget on the left for the different neighborhoods)
boston_neighborhoods = airbnb_data['neighbourhood'].unique()
user_selected_neighborhood = st.sidebar.selectbox("Select a Neighborhood", boston_neighborhoods)


# [ST2] Slider widget for the minimum and maximum price (User can adjust the price to their liking)
airbnb_price_range = st.sidebar.slider(
    "Select a Price Range",
    min_value=int(airbnb_data['price'].min()),
    max_value=int(airbnb_data['price'].max()),
    value=(int(airbnb_data['price'].min()), int(airbnb_data['price'].max()))
)


# [ST3] Slider widget for minimum nights (Minimum Nights = Nights required to stay)
minimum_night_count = st.sidebar.slider(
    "Select a Minimum Number of Nights",
    min_value=int(airbnb_data['minimum_nights'].min()),
    max_value=int(airbnb_data['minimum_nights'].max()),
    value=(int(airbnb_data['minimum_nights'].min()), int(airbnb_data['minimum_nights'].max()))
)



# [DA5] Filter data by two or more conditions
# Filtering the AirBnB data
filtered_airbnb_data = airbnb_data[
    (airbnb_data['neighbourhood'] == user_selected_neighborhood) &
    (airbnb_data['price'] >= airbnb_price_range[0]) &
    (airbnb_data['price'] <= airbnb_price_range[1]) &
    (airbnb_data['minimum_nights'] >= minimum_night_count[0]) &
    (airbnb_data['minimum_nights'] <= minimum_night_count[1])
]

# Error code for empty data, occurs when the minimum price range is too high
# and there are no available properties in that specific selected neighborhood
# below is the error message that will appear above the map
if filtered_airbnb_data.empty:
    st.error("No properties were found with the selected filters (check price slider). The minimum price may be too high, "
             "please adjust your filters until the map re-appears, or reload the website.")

# Pydeck Map Visualization
st.subheader("Map of Available Properties in Boston")

map_airbnb_property_data = filtered_airbnb_data[['latitude', 'longitude', 'price', 'minimum_nights', 'number_of_reviews', 'name', 'neighbourhood',
                                                 'room_type', 'host_name', 'last_review', 'availability_365']]

# [MAP] Detailed map with Pydeck + Interactable + Updates with user selected filters
layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_airbnb_property_data,
    get_position='[longitude, latitude]',
    get_radius=25,
    get_fill_color='[0, 255, 0, 160]',
    pickable=True
)

view_state = pdk.ViewState(
    latitude=map_airbnb_property_data['latitude'].mean(),
    longitude=map_airbnb_property_data['longitude'].mean(),
    zoom=11,
    pitch=0
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={ "text": "Name: {name}\nNeighborhood: {neighbourhood}\nRoom Type: {room_type}\n"
                 "Host: {host_name}\nPrice: ${price}\nNights: {minimum_nights}\n"
                 "Reviews: {number_of_reviews}\nLast Review: {last_review}\n"
                 "Availability (365 days): {availability_365}"}
    # For when you hover over the tiny dots on the map and some important listing information pops up
)

st.pydeck_chart(r)
st.write("Map Description: "
         "The map above displays available properties for renting by selected neighborhood. The green dots indicate a listing, "
         "and you can hover over them to see important details such as the listing name, neighborhood, price, minimum nights required, number of reviews, etc. "
         "Use the filters to adjust the displayed properties based on your preferences.")
            # Description for the AirBnB Property Map and how to understand it

# Price distribution chart (Matplotlib Distribution Chart)
# X-axis is Price / Y-axis is Frequency (listings)
st.subheader("Price Distribution in Selected Neighborhood")
plt.figure(figsize=(10, 6))
plt.plot(filtered_airbnb_data['price'].value_counts().sort_index(), color='orange')
plt.xlabel("Price ($)")
plt.ylabel("Frequency")
plt.title("Price Distribution in Selected Neighborhood")
st.pyplot(plt)
st.write("Price Distribution Chart Description: "
         "The chart above displays the distribution of prices for Airbnb properties in the selected neighborhood. "
         "The frequency shows how often properties are listed at different price points, helping you understand the "
         "pricing trends and identify common price ranges to help you in your decision making process.")
            # Description for the Price Distribution Chart and how to understand it


# Average price by neighborhood (Streamlit Bar Chart)
st.subheader("Average Price by Neighborhood")

# [DA2] Sort data in ascending order
avg_property_rental_price = airbnb_data.groupby('neighbourhood')['price'].mean().sort_values()
st.bar_chart(avg_property_rental_price)
st.write("Bar Chart Description: "
         "The bar chart above displays various AirBnB locations in Boston, "
         "based on average price and by each neighborhood. "
         "It helps you compare which areas are generally more expensive or affordable for short-term rentals, "
         "providing insights into the overall market landscape.")
            # Description for the bar chart and how to understand it


# [VIZ1] Pie chart for the different room types (Streamlit Pie Chart)
st.subheader("Room Type Distribution in Selected Neighborhood")

room_type_versions = filtered_airbnb_data['room_type'].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(room_type_versions, labels=room_type_versions.index, autopct='%1.1f%%', startangle=90)
plt.title("Room Type Distribution")
st.pyplot(plt)
st.write("Pie Chart Description: "
         "The pie chart above displays the different room types in the selected neighborhood. "
         "The chart can give you some insight into the different room types in the area, "
         "such as Entire homes/apt, Private rooms, Hotel rooms, or Shared rooms. "
         "Below you can view the different listings for room types and the min/max price for all the properties together.")
            # Description for the Pie Chart and how to understand it


# [PY1] A function with two or more parameters, one with a default value
def filter_by_property_reviews(data, min_reviews=0, max_reviews=1000):
    return data[(data['number_of_reviews'] >= min_reviews) & (data['number_of_reviews'] <= max_reviews)]


# The function for reviews
# Pretty much filters the reviews and returns a new filter range between 10-50 reviews.
filtered_property_reviews_data = filter_by_property_reviews(airbnb_data, 10, 50)
default_property_reviews_data = filter_by_property_reviews(airbnb_data)


# [PY3] Error checking with try/except for the price ranges to ensure no errors
# Also works as price insight for the user at the bottom of the website
try:
    min_price, max_price = airbnb_price_statistics(airbnb_data)
    st.write(f"**Minimum Price:** ${min_price:.2f}")
    st.write(f"**Maximum Price:** ${max_price:.2f}")
except Exception as e:
    st.error(f"An error has occurred: {e}")

# [PY4] List comprehension for the different room types
# also works as insight for the user on the different room types mainly for the pie chart
unique_property_room_types = [property_room_type for property_room_type in airbnb_data['room_type'].unique()]


# [PY5] Using a dictionary
# also works as insight for the user on the different room types mainly for the pie chart
property_room_type_dict = {room_type: airbnb_data[airbnb_data['room_type'] == room_type] for room_type in unique_property_room_types}
st.write("Room Types and Listings:", list(property_room_type_dict.keys()))

# Little Paragraph at the bottom of the website for the user to read,
# ends/closes the story
st.subheader("Understanding Boston's AirBnB Market")
st.write("Utilizing the various charts and map visualizations from above, "
         "we're able to learn quite a lot about Boston's AirBnb Market. "
         "We can learn about the costs of the different areas in Boston to gain a better "
         "understanding of the rental landscape. Also, an area that has more reviews could "
         "potentially mean it's more of a hotspot to stay in. Understanding these variables "
         "can help us gain a better insight into the Boston AirBnB market. "
         "I hope this data can help you in your decision making process or expand your interest in "
         "learning about Boston's AirBnB market!")