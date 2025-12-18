import pandas as pd
from recommender import SHLRecommender

def evaluate_and_generate_submission():
   
    try:
        
        test_df = pd.read_excel('Gen_AI Dataset.xlsx')
        
        
        print("\n Found Columns in Excel:", test_df.columns.tolist())
        
        
        query_col = None
        for col in test_df.columns:
            if "query" in col.lower() or "question" in col.lower() or "prompt" in col.lower():
                query_col = col
                break
        
        
        if not query_col:
            query_col = test_df.columns[0]
            print(f" 'Query' column not explicitly found. Defaulting to first column: '{query_col}'")
        else:
            print(f"Using column '{query_col}' as the query source.")
            
    except Exception as e:
        print(f"Error loading file: {e}")
        return

   
    engine = SHLRecommender()
    submission_rows = []

    print(f"Processing {len(test_df)} test queries...")

    for index, row in test_df.iterrows():
       
        query_text = str(row[query_col]) 
        
        if not query_text.strip():
            continue
            
        print(f"   Query {index + 1}: {query_text[:50]}...")
        
        
        results = engine.get_recommendations(query_text, k=10)
        
       
        for rec in results:
            submission_rows.append({
                "Query": query_text,
                "Assessment_url": rec['URL']
            })

    
    submission_df = pd.DataFrame(submission_rows)
    
    submission_df = submission_df[['Query', 'Assessment_url']]
    
    submission_df.to_csv("submission.csv", index=False)
    print("\n'submission.csv' generated successfully!")

if __name__ == "__main__":
    evaluate_and_generate_submission()