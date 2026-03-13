import pandas as pd
import os

def create_mock_excel():
    # ------------- MASTER PARTICIPANT LIST -------------
    # Add ALL possible participants here.
    # Speaker_Label is the expected assignment (A, B, C...).
    # Only people whose label appears in the transcript will be emailed.
    data = {
        "Speaker_Label": ["Speaker A", "Speaker B", "Speaker C", "Speaker D", "Speaker E", "Speaker F", "Speaker G", "Speaker H"],
        "Name":          ["alex",      "jamie",     "sam",       "cassey",    "lohith",    "shreya",    "samruddhi", "gagan"     ],
        "Email":         ["learningtraverse@gmail.com", "lohithnandyal1@gmail.com", "leematans05@gmail.com",
                          "srujana.hm15@gmail.com", "dishahali075@gmail.com", "nandyallohith@gmail.com",
                          "samruddhims1111@gmail.com", "shreyaanadkumar3@gmail.com"]
    }
    # -----------------------------------------------
    
    df = pd.DataFrame(data)
    
    file_path = "participants.xlsx"
    df.to_excel(file_path, index=False)
    print(f"Excel file created with custom emails at: {os.path.abspath(file_path)}")

if __name__ == "__main__":
    create_mock_excel()
