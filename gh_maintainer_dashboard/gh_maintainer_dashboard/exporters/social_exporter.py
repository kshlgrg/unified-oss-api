from gh_maintainer_dashboard.models.cv import CVData


class SocialExporter:
    def generate_linkedin_text(self, cv_data: CVData) -> str:
        text = f"""🎉 Proud to share my Open Source Maintainer journey!

As an active maintainer of {cv_data.professional_summary.repos_maintained} repositories, I've had the privilege of:

✅ Conducting {cv_data.professional_summary.total_reviews}+ code reviews
🤝 Mentoring {cv_data.professional_summary.contributors_mentored} contributors
🛠️ Managing {cv_data.professional_summary.total_maintenance_work} maintenance activities

Key contributions include:
"""
        for achievement in cv_data.achievements[:3]:
            text += f"• {achievement}\n"
        
        text += f"\nCheck out my profile: {cv_data.maintainer_info.github_url}\n\n"
        text += "#OpenSource #SoftwareEngineering #CommunityBuilding #CodeReview"
        
        return text
    
    def generate_twitter_text(self, cv_data: CVData) -> str:
        text = f"""🚀 Open Source Maintainer Update!

📊 {cv_data.professional_summary.total_reviews} reviews
🤝 {cv_data.professional_summary.contributors_mentored} mentees
🏗️ {cv_data.professional_summary.repos_maintained} repos

Proud to contribute to the #OpenSource community!

{cv_data.maintainer_info.github_url}
"""
        return text
