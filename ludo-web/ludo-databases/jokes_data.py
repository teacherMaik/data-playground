import pandas as pd
import json

with open('dumps/dump-jokes-2025-05-20.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


df_all_jokes = pd.DataFrame(data['all_jokes'])
df_reactions_en = pd.DataFrame(data['jokes_reactions_en'])
df_reactions_es = pd.DataFrame(data['jokes_reactions_es'])

# print(df_all_jokes)
# print(df_reactions_en)
# print(df_reactions_es)

df_reactions_es['joke_lang'] = 'es'
df_reactions_en['joke_lang'] = 'en'

df_reactions = pd.concat([df_reactions_en, df_reactions_es], ignore_index=True)

print(df_reactions)

# Step 3: Group by joke_id, joke_lang, and reaction type
reaction_counts = df_reactions.groupby(['joke_id', 'joke_lang', 'joke_reaction']) \
                              .size() \
                              .unstack(fill_value=0) \
                              .reset_index()

# Step 4: Rename columns to avoid issues
reaction_counts = reaction_counts.rename(columns={
    'laugh': 'laugh',
    'no-laugh': 'no_laugh'
})

print(reaction_counts)

df_all_jokes_reactions = df_all_jokes.merge(reaction_counts, on = ['joke_id', 'joke_lang'], how = 'left')

print(df_all_jokes_reactions)

df_all_jokes_reactions['laugh'] = df_all_jokes_reactions['laugh'].fillna(0).astype(int)
df_all_jokes_reactions['no_laugh'] = df_all_jokes_reactions['no_laugh'].fillna(0).astype(int)

print(df_all_jokes_reactions)

df_all_jokes_reactions['total_reactions'] = df_all_jokes_reactions['laugh'] + df_all_jokes_reactions['no_laugh']

print(df_all_jokes_reactions)

print(f"Total Reactions {df_all_jokes_reactions['total_reactions'].sum()}")
print(f"Joke with most reactions is {df_all_jokes_reactions['total_reactions'].max()}")

print(df_all_jokes_reactions.sort_values(by='laugh', ascending=False).head(1))
print(df_all_jokes_reactions.groupby('joke_lang')['total_reactions'].mean())
print(df_all_jokes_reactions.groupby('date')['total_reactions'].sum())