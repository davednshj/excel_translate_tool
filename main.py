import pandas as pd
from deep_translator import GoogleTranslator
import numpy as np
from tqdm import tqdm
import time

def translate_text(text, target_lang='es'):
    """Translate text while handling non-string values"""
    if pd.isna(text) or not isinstance(text, str):
        return text
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        return translator.translate(text)
    except:
        return text

def translate_excel(input_file, output_file, target_lang='es'):
    print(f"Loading Excel file: {input_file}")
    df = pd.read_excel(input_file)
    
    translated_df = df.copy()
    total_columns = len(df.columns)
    
    print(f"\nTranslating {total_columns} columns...")
    start_time = time.time()
    
    # Add progress bar for columns
    for column in tqdm(translated_df.columns, desc="Processing columns"):
        non_null_count = translated_df[column].count()
        if non_null_count > 0:
            print(f"\nTranslating column: {column} ({non_null_count} cells)")
            translated_df[column] = translated_df[column].progress_apply(
                lambda x: translate_text(x, target_lang)
            )
    
    elapsed_time = time.time() - start_time
    print(f"\nTranslation completed in {elapsed_time:.2f} seconds")
    
    print(f"Saving to: {output_file}")
    translated_df.to_excel(output_file, index=False)
    return "Translation completed successfully!"

if __name__ == "__main__":
    input_file = "/Users/daviddanishjo/Documents/GitHub/excel_translate_tool/Novelties 2025 H1.xlsx"
    output_file = "translated_output.xlsx"
    
    # Enable tqdm for pandas
    tqdm.pandas()
    
    result = translate_excel(input_file, output_file, target_lang='de')
    print(result)

