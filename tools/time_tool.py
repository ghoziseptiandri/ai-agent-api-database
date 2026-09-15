from datetime import datetime

def get_current_time() -> str:
    print("🕒 Time tool called!")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")