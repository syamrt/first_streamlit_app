import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt');
my_fruit_list = my_fruit_list.set_index('Fruit');
streamlit.title('Indian Healthy Diner');

streamlit.header('Breakfast Menu');
streamlit.text('Omega 3 & Blueberry Oatmeal');
streamlit.text('Kale, Spinach & Rocket Smoothie');
streamlit.text('Hard-Boiled Free-Range Egg');

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇');
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized;
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    back_from_function = get_fruitvice_data(fruit_choice)
  #streamlit.write('The user entered ', fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()
  

streamlit.text("The fruit load list contains:")
# snowflake related functions:
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

#add a button to load fruits
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list();
  streamlit.dataframe(my_data_rows)

#stremlit.text('Hii')
#streamlit.stop();
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('from streamlist')")
    return 'Thanks for adding '+ new_fruit;
    
#streamlit.text("Hi")
add_my_fruit = streamlit.text_input('Which fruit would you like to add ?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
