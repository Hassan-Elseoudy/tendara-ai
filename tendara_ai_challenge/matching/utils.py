import json
from datetime import datetime
from pathlib import Path
from typing import List

from tendara_ai_challenge.matching.dto import NoticeModel


def load_notices() -> List[NoticeModel]:
    """
    Loads tender notices from the test_notices.json file and converts them to Notice objects.
    
    Returns:
        List[Notice]: A list of Notice objects containing the tender data
    """
    data_path = Path(__file__).parent.parent / "data" / "notices.json"
    
    with open(data_path, "r", encoding="utf-8") as f:
        notices_data = json.load(f)
    
    notices = []
    for notice_data in notices_data:
        notice_data["publication_deadline"] = datetime.fromisoformat(notice_data["publication_deadline"])
        notice_data["submission_deadline"] = datetime.fromisoformat(notice_data["submission_deadline"])
        
        notice = NoticeModel(**notice_data)
        notices.append(notice)
    
    return notices

def pretty_print_notices(notices: List[NoticeModel]) -> None:
    """
    Pretty prints a list of notices in a readable format.
    
    Args:
        notices (List[Notice]): List of Notice objects to display
    """
    for i, notice in enumerate(notices, 1):
        print(f"\n=== Notice {i} ===")
        print(f"Title: {notice.title}")
        print(f"Description: {notice.description}")
        print(f"Publication Deadline: {notice.publication_deadline}")
        print(f"Submission Deadline: {notice.submission_deadline}")
        print(f"CPV Codes: {', '.join(notice.cpv_codes)}")
        print("=" * 50)
