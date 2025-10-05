from datetime import datetime, timedelta
from typing import List, Tuple


class DateHelpers:
    @staticmethod
    def parse_date(date_string: str) -> datetime:
        formats = [
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_string}")
    
    @staticmethod
    def format_date(date: datetime, format_string: str = "%Y-%m-%d") -> str:
        return date.strftime(format_string)
    
    @staticmethod
    def get_date_range(period: str) -> Tuple[datetime, datetime]:
        end_date = datetime.now()
        
        if period.endswith("d"):
            days = int(period[:-1])
            start_date = end_date - timedelta(days=days)
        elif period.endswith("w"):
            weeks = int(period[:-1])
            start_date = end_date - timedelta(weeks=weeks)
        elif period.endswith("m"):
            months = int(period[:-1])
            start_date = end_date - timedelta(days=months * 30)
        elif period.endswith("y"):
            years = int(period[:-1])
            start_date = end_date - timedelta(days=years * 365)
        else:
            start_date = end_date - timedelta(days=30)
        
        return start_date, end_date
    
    @staticmethod
    def generate_date_list(start_date: datetime, end_date: datetime) -> List[str]:
        date_list = []
        current_date = start_date
        
        while current_date <= end_date:
            date_list.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)
        
        return date_list
    
    @staticmethod
    def get_week_boundaries(date: datetime) -> Tuple[datetime, datetime]:
        start_of_week = date - timedelta(days=date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return start_of_week, end_of_week
    
    @staticmethod
    def is_weekend(date: datetime) -> bool:
        return date.weekday() >= 5
    
    @staticmethod
    def get_hour(date: datetime) -> int:
        return date.hour
    
    @staticmethod
    def days_between(date1: datetime, date2: datetime) -> int:
        return abs((date2 - date1).days)
