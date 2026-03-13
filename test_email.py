import os
from email_agent import load_participant_data, dispatch_meeting_notes
from generate_mock_excel import create_mock_excel

if __name__ == "__main__":
    excel_file = "participants.xlsx"
    if not os.path.exists(excel_file):
        print("Mock Excel file not found. Generating one...")
        create_mock_excel()
        
    print("Loading participant data...")
    participant_dict = load_participant_data(excel_file)
    print("Participant Data Loaded:", participant_dict)
    
    mock_summary = "We discussed the final rollout of the Multi-Modal Meeting Assistant. We agreed on the core architecture for the LangChain integration and set dates for the beta launch. We also walked through the email dispatcher agent logic."
    
    mock_action_items = [
        {"task": "Design Database Schema", "assignee": "Speaker A", "deadline": "Monday"},
        {"task": "Write Email Dispatcher module", "assignee": "Speaker B", "deadline": "Tuesday"},
        {"task": "Prepare slide deck for demo", "assignee": "Speaker C", "deadline": "Wednesday"},
        {"task": "Test LangChain pipeline", "assignee": "Speaker A", "deadline": "Friday"}
    ]
    
    print("\nDispatching meeting notes...")
    dispatch_meeting_notes(mock_summary, mock_action_items, participant_dict)
    
    print("\nTest completed.")
