import pandas as pd
import os

def create_mock_excel():
    # ------------- EDIT YOUR EMAILS HERE -------------
    data = {
        "Speaker_Label": ["Speaker A", "Speaker B", "Speaker C"],
        "Name": ["Name A", "Name B", "Name C"],
        "Email": ["your_first_email@company.com", "your_second_email@company.com", "your_third_email@company.com"]
    }
    # -----------------------------------------------
    
    df = pd.DataFrame(data)
    
    file_path = "participants.xlsx"
    df.to_excel(file_path, index=False)
    print(f"Excel file created with custom emails at: {os.path.abspath(file_path)}")

if __name__ == "__main__":
    create_mock_excel()
