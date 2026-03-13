import pandas as pd
import os

def create_mock_excel():
    data = {
        "Speaker_Label": ["Speaker A", "Speaker B", "Speaker C"],
        "Name": ["Jash", "Chinnmay", "Alice"],
        "Email": ["jash@example.com", "chinnmay@example.com", "alice.test@example.com"]
    }
    
    df = pd.DataFrame(data)
    
    file_path = "participants.xlsx"
    df.to_excel(file_path, index=False)
    print(f"Mock Excel file created successfully at: {os.path.abspath(file_path)}")

if __name__ == "__main__":
    create_mock_excel()
