import json
from typing import Dict, Any


class JSONExporter:
    @staticmethod
    def export(data: Dict[str, Any], pretty: bool = True) -> str:
        if pretty:
            return json.dumps(data, indent=2, default=str)
        return json.dumps(data, default=str)
    
    @staticmethod
    def export_to_file(data: Dict[str, Any], filename: str, pretty: bool = True) -> None:
        with open(filename, 'w') as f:
            if pretty:
                json.dump(data, f, indent=2, default=str)
            else:
                json.dump(data, f, default=str)
