import fnmatch
import pandas as pd
import glob
import streamlit as st

st.title("Spellchecker 1.0.0")
st.write("Type any word to check spelling. Use '?' for unknown letters.")

csv_files = glob.glob("*.csv")
combined_df = pd.concat(
	map(lambda file: pd.read_csv(file, header=None, dtype=str, encoding="cp1252"), csv_files), ignore_index=True)

combined_df[0] = combined_df[0].str.lower()
new_df = combined_df[0].str.split(" ", n=1, expand=True)

user_query = st.text_input("Spell a word: ").lower()
user_match = list(dict.fromkeys(fnmatch.filter(new_df[0].dropna().tolist(), user_query)))

if user_query == "":
	st.write("")
else:
	if user_match == []:
		st.write("No matches found.")
	else:
		st.write(f"Matches: {', '.join(user_match)}\n")
		user_choice = st.text_input("View definition(s)? Y/N: ").lower()
		if user_choice == "y":
			for word in user_match:
				matched_definitions = new_df.loc[new_df[0] == word, 1].tolist()
				formatted_output = "\n".join([f"{i}. {definition}" for i, definition in enumerate(matched_definitions, start=1)])
				st.write(f"\n{word}\n{formatted_output}\n")

st.markdown("""
<style>
    /* Remove background, borders, and make the actual typing text invisible */
    .stTextInput input {
        background-color: transparent !important;
        border: none !important;
        color: transparent !important; /* Hide original letters */
        caret-color: #31333E !important; /* Keep the blinking vertical typing cursor visible */
        font-size: 24px !important;
        font-family: monospace !important;
        letter-spacing: 16px; /* Match spacing of our colored boxes */
        padding-left: 15px !important;
        position: absolute;
        z-index: 2;
    }
    /* Hide the focused blue border outline that Streamlit adds */
    .stTextInput div[data-baseweb="input"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Add an empty container that will house our stacked elements
container = st.container()

with container:
    # 3. Create the input widget. The user types here, but the letters are invisible!
    user_query = st.text_input("Type your letters here:", value="Hello")
    
    # 4. Generate the styled colored boxes using the text the user just typed
    vowels = "AEIOUaeiou"
    
    # This background container mirrors exactly where the user is typing
    annotated_html = '<div style="display: flex; flex-wrap: wrap; gap: 8px; font-size: 24px; font-weight: bold; font-family: monospace; position: relative; top: -45px; z-index: 1; pointer-events: none;">'
    
    for letter in user_input:
        if letter == " ":
            annotated_html += '<div style="width: 18px;"></div>'
        elif letter.isalpha():
            if letter in vowels:
                # Yellow boxes for vowels
                annotated_html += f'<div style="background-color: #FFDE4D; color: #000000; width: 35px; height: 45px; display: flex; align-items: center; justify-content: center; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">{letter}</div>'
            else:
                # Blue boxes for consonants
                annotated_html += f'<div style="background-color: #3FA2F6; color: #FFFFFF; width: 35px; height: 45px; display: flex; align-items: center; justify-content: center; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">{letter}</div>'
        else:
            # Special characters or numbers
            annotated_html += f'<div style="width: 35px; height: 45px; display: flex; align-items: center; justify-content: center; color: #888888;">{letter}</div>'
            
    annotated_html += '</div>'
    
    # 5. Render the HTML layer directly underneath the invisible typing layer
    st.html(annotated_html)
