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

# 2. Define vowels
vowels = "AEIOUaeiou"

# 3. Create a container to hold the letters side-by-side
# We use HTML flexbox so the letters wrap neatly onto the next line
annotated_html = '<div style="display: flex; flex-wrap: wrap; gap: 8px; font-size: 24px; font-weight: bold; font-family: monospace;">'

# 4. Loop through every letter the user typed
for letter in user_input:
    # Handle spaces (keep them as invisible gaps)
    if letter == " ":
        annotated_html += '<div style="width: 15px;"></div>'
    # Check if the character is a letter
    elif letter.isalpha():
        if letter in vowels:
            # Yellow box for vowels
            annotated_html += f'<div style="background-color: #FFDE4D; color: #000000; padding: 10px 15px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">{letter}</div>'
        else:
            # Blue box for consonants
            annotated_html += f'<div style="background-color: #3FA2F6; color: #FFFFFF; padding: 10px 15px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">{letter}</div>'
    else:
        # Keep numbers and punctuation without special colored boxes
        annotated_html += f'<div style="padding: 10px 5px; color: #888888;">{letter}</div>'

annotated_html += '</div>'

# 5. Render the styled HTML boxes directly on the screen
st.html(annotated_html)
