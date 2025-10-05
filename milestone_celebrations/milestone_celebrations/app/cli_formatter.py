from typing import Dict, List

class CLIFormatter:
    @staticmethod
    def format_milestones_table(data: Dict) -> str:
        output = []
        
        sections = data.get("sections", {})
        
        for section_name, section_data in sections.items():
            output.append(f"\n{'='*80}")
            output.append(f"  📍 SECTION: {section_name.upper()}")
            output.append(f"{'='*80}\n")
            
            if section_data.get("milestones"):
                output.append(CLIFormatter._create_milestone_table(section_data["milestones"]))
            
            if section_data.get("upcoming"):
                output.append(f"\n{'─'*80}")
                output.append(f"  🎯 UPCOMING MILESTONES")
                output.append(f"{'─'*80}\n")
                output.append(CLIFormatter._create_upcoming_table(section_data["upcoming"]))
        
        return "\n".join(output)
    
    @staticmethod
    def _create_milestone_table(milestones: List[Dict]) -> str:
        header = f"{'Icon':<6} {'Type':<20} {'Title':<40} {'Count':<8} {'Status':<12}"
        separator = "─" * 90
        
        rows = [header, separator]
        
        for m in milestones:
            icon = m.get("icon", "")
            mtype = m.get("type", "")[:20]
            title = m.get("title", "")[:40]
            count = str(m.get("count", ""))
            status = "✅ Celebrated" if m.get("celebrated") else "🆕 NEW!"
            
            row = f"{icon:<6} {mtype:<20} {title:<40} {count:<8} {status:<12}"
            rows.append(row)
        
        return "\n".join(rows)
    
    @staticmethod
    def _create_upcoming_table(upcoming: List[Dict]) -> str:
        header = f"{'Icon':<6} {'Title':<40} {'Progress':<25} {'Remaining':<10}"
        separator = "─" * 90
        
        rows = [header, separator]
        
        for u in upcoming:
            icon = u.get("icon", "")
            title = u.get("title", "")[:40]
            current = u.get("current", 0)
            target = u.get("next_milestone", 0)
            remaining = u.get("remaining", 0)
            progress = f"{current}/{target} ({int(current/target*100)}%)" if target > 0 else "N/A"
            
            row = f"{icon:<6} {title:<40} {progress:<25} {remaining:<10}"
            rows.append(row)
        
        return "\n".join(rows)
