import pandas as pd
import re


input_file = "shl_assessments.csv"
output_file = "shl_assessments_preprocessed.csv"

try:
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} rows from {input_file}")
except FileNotFoundError:
    print(f"Error: {input_file} not found. Please run the scraper first.")
    exit()


type_mapping = {
    'K': 'Knowledge & Skills',
    'P': 'Personality & Behavior',
    'A': 'Ability & Aptitude',
    'B': 'Biodata & Situational Judgement',
    'S': 'Simulations',
    'C': 'Competencies',
    'D': 'Development & 360',
    'E': 'Assessment Exercises',
   
    'Ability': 'Ability & Aptitude',
    'Skill': 'Knowledge & Skills'
}

def clean_type(t):
    """Converts code like 'K' to 'Knowledge & Skills'"""
    
    t_str = str(t).strip()
    return type_mapping.get(t_str, t_str)

df['test_type_full'] = df['test_type'].apply(clean_type)


df['combined_text'] = (
    "Assessment Name: " + df['name'].fillna("Unknown") + ". " +
    "Type: " + df['test_type_full'] + ". " +
    "Description: " + df['description'].fillna("No description available.")
)


df['combined_text'] = df['combined_text'].apply(lambda x: re.sub(r'\s+', ' ', x).strip())


df.to_csv(output_file, index=False)

print("\n--- Preprocessing Complete ---")
print(f"Processed data saved to: {output_file}")
print("Sample Entry:")
print(df['combined_text'].iloc[0])