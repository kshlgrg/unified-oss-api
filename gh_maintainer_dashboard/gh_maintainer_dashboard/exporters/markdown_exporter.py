from gh_maintainer_dashboard.models.cv import CVData


class MarkdownExporter:
    def export_cv(self, cv_data: CVData) -> str:
        md = []
        
        md.append(f"# {cv_data.maintainer_info.name}")
        md.append(f"**{cv_data.maintainer_info.title}**\n")
        
        if cv_data.maintainer_info.location:
            md.append(f"📍 {cv_data.maintainer_info.location}")
        md.append(f"🔗 [{cv_data.maintainer_info.github_url}]({cv_data.maintainer_info.github_url})\n")
        
        md.append("## Professional Summary\n")
        md.append(cv_data.professional_summary.summary_text + "\n")
        
        md.append("### Key Metrics\n")
        md.append(f"- **Total Reviews**: {cv_data.professional_summary.total_reviews}")
        md.append(f"- **Repositories Maintained**: {cv_data.professional_summary.repos_maintained}")
        md.append(f"- **Contributors Mentored**: {cv_data.professional_summary.contributors_mentored}")
        md.append(f"- **Total Maintenance Work**: {cv_data.professional_summary.total_maintenance_work}\n")
        
        md.append("## Invisible Labor Breakdown\n")
        for item in cv_data.invisible_labor_breakdown:
            md.append(f"- **{item.category}**: {item.count} ({item.percentage}%)")
        md.append("")
        
        if cv_data.key_repositories:
            md.append("## Key Repositories\n")
            for repo in cv_data.key_repositories:
                md.append(f"### {repo.name}")
                md.append(f"**Role**: {repo.role}")
                md.append(f"**Duration**: {repo.duration}")
                md.append(f"**Contributions**: {repo.contributions}")
                md.append(f"**Impact**: {repo.impact}\n")
        
        md.append("## Achievements\n")
        for achievement in cv_data.achievements:
            md.append(f"- {achievement}")
        md.append("")
        
        md.append("## Skills Demonstrated\n")
        for skill in cv_data.skills_demonstrated:
            md.append(f"- {skill}")
        
        return "\n".join(md)
    
    def export_profile_readme(self, profile_data: dict) -> str:
        md = []
        
        md.append("# 👨‍💻 Maintainer Profile\n")
        md.append("## 📊 Maintainer Statistics\n")
        
        stats = profile_data.get("summary_stats", {})
        md.append(f"- 🔍 **Code Reviews**: {stats.get('total_reviews', 0)}")
        md.append(f"- 🎯 **Issues Triaged**: {stats.get('total_issues_triaged', 0)}")
        md.append(f"- 🎓 **Contributors Mentored**: {stats.get('mentorship_interactions', 0)}")
        md.append(f"- 📚 **Documentation Contributions**: {stats.get('documentation_contributions', 0)}")
        md.append(f"- 🏗️ **Repositories Maintained**: {stats.get('total_repos_maintained', 0)}\n")
        
        return "\n".join(md)
