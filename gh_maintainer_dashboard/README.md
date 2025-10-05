# GitHub Maintainer Dashboard

A comprehensive Python package for tracking and analyzing GitHub repository maintainer activities.

## Features

- Track all maintainer activities (reviews, issue triage, mentorship, documentation)
- Sentiment analysis on PR reviews
- Find similar maintainers based on tech stack and interests
- Generate shareable maintainer CVs
- Milestone celebrations and badges
- Repository breakdown and time series analysis

## Installation

## Quick Start

from gh_maintainer_dashboard import MaintainerDashboard

dashboard = MaintainerDashboard(github_token="your_github_token")

profile = dashboard.get_profile("octocat")
print(profile.summary_stats)

text

## Configuration

Create a `.env` file:

GITHUB_TOKEN=your_github_personal_access_token

text

## License

MIT License