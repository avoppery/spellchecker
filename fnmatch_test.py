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
	st.write([])
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
