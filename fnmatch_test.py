import fnmatch
import pandas as pd
import glob

csv_files = glob.glob("*.csv")
combined_df = pd.concat(
	map(lambda file: pd.read_csv(file, header=None, dtype=str, encoding="cp1252"), csv_files), ignore_index=True)

combined_df[0] = combined_df[0].str.lower()
new_df = combined_df[0].str.split(" ", n=1, expand=True)

print("Input Text")

user_query = input().lower()
user_match = list(dict.fromkeys(fnmatch.filter(new_df[0].dropna().tolist(), user_query)))

if user_match == []:
	print("No matches found.")
else:
	print(f"Matches: {', '.join(user_match)}\n")
	print("View Definition(s)? Y/N")
	user_choice = input().lower()
	if user_choice == "y":
		for word in user_match:
			matched_definitions = new_df.loc[new_df[0] == word, 1].tolist()
			formatted_output = "\n".join([f"{i}. {definition}" for i, definition in enumerate(matched_definitions, start=1)])
			print(f"\n{word}\n{formatted_output}\n")