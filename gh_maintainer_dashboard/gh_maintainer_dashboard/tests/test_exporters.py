import pytest
from gh_maintainer_dashboard.exporters.json_exporter import JSONExporter
from gh_maintainer_dashboard.exporters.markdown_exporter import MarkdownExporter
from gh_maintainer_dashboard.models.cv import CVData, MaintainerInfo, ProfessionalSummary


class TestJSONExporter:
    def test_export_pretty(self):
        data = {"name": "test", "value": 123}
        result = JSONExporter.export(data, pretty=True)
        
        assert "test" in result
        assert "123" in result
        assert "\n" in result
    
    def test_export_compact(self):
        data = {"name": "test", "value": 123}
        result = JSONExporter.export(data, pretty=False)
        
        assert "test" in result
        assert "123" in result


class TestMarkdownExporter:
    def setup_method(self):
        self.exporter = MarkdownExporter()
        
        self.cv_data = CVData(
            maintainer_info=MaintainerInfo(
                name="Test User",
                username="testuser",
                github_url="https://github.com/testuser",
            ),
            professional_summary=ProfessionalSummary(
                total_reviews=100,
                repos_maintained=5,
                contributors_mentored=20,
                summary_text="Test summary"
            )
        )
    
    def test_export_cv(self):
        result = self.exporter.export_cv(self.cv_data)
        
        assert "Test User" in result
        assert "Professional Summary" in result
        assert "100" in result
        assert "testuser" in result
    
    def test_export_profile_readme(self):
        profile_data = {
            "summary_stats": {
                "total_reviews": 100,
                "total_issues_triaged": 50,
                "mentorship_interactions": 20,
            }
        }
        
        result = self.exporter.export_profile_readme(profile_data)
        
        assert "Maintainer Profile" in result
        assert "100" in result
