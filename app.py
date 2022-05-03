import webbrowser
import streamlit as st
import pickle
import pandas as pd

recipes_dict = pickle.load(open('recipe_dict.pkl', 'rb'))
recipes = pd.DataFrame(recipes_dict)
similarity = pickle.load(open('similarity_recipe.pkl', 'rb'))

def recommend(recipe):
    reqIndex = recipes[recipes['TranslatedRecipeName'] == recipe].index[0]
    distances = similarity[reqIndex]
    list1 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_recipes = []
    recipe_images = []
    recipe_url = []
    for i in list1:
        recipe_url.append(recipes.iloc[i[0]]['URL'])
        recipe_images.append(recipes.iloc[i[0]]['Image_Url'])
        recommended_recipes.append(recipes.iloc[i[0]]['TranslatedRecipeName'])
    return recommended_recipes, recipe_images, recipe_url

st.title('Find a perfect recipe here!')

selected_recipe_name = st.selectbox('Select recipe', (recipes['TranslatedRecipeName'].values))
selected_recipe_url = (recipes['URL'][recipes['TranslatedRecipeName'] == selected_recipe_name]).values[0]
selected_recipe_image_url = (recipes['Image_Url'][recipes['TranslatedRecipeName'] == selected_recipe_name]).values[0]

if st.button(selected_recipe_name):
    webbrowser.open_new_tab(selected_recipe_url)
st.image(selected_recipe_image_url, width=500)

if st.button('Get recommendations'):
    st.title("Here are some recommendations for you!")
    recommendations,images, recipe_url = recommend(selected_recipe_name)

    for i in range(0,len(recommendations)):
        if st.button(recommendations[i]):
            webbrowser.open_new_tab(recipe_url[i])
        st.image(images[i], width=300)




