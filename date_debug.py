from datetime import datetime

def parse_date(date_string):
    """Parse date string and return Python date object"""
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()
        print(f"Successfully parsed '{date_string}' to {date_obj} (type: {type(date_obj)})")
        return date_obj
    except ValueError as e:
        print(f"Error parsing date: {str(e)}")
        return None

# Test with dates
if __name__ == "__main__":
    test_dates = ['2025-04-08', '04/08/2025', '2025/04/08', '08-04-2025']
    
    print("Testing date parsing:")
    for date_str in test_dates:
        result = parse_date(date_str)
        if result:
            print(f"✓ {date_str} -> {result}")
        else:
            print(f"✗ {date_str} -> Failed")
