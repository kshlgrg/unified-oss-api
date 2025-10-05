from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

from gh_maintainer_dashboard import MaintainerDashboard
from milestone_celebrations import MilestoneCelebrations
from cookie_licking_detector import CookieLickingDetector
from oss_discovery_engine import OSSDiscoveryEngine

app = Flask(__name__)
CORS(app)

TOKEN = os.getenv('GITHUB_TOKEN')

@app.route('/')
def home():
    return jsonify({
        "status": "API Running",
        "version": "1.0.0",
        "endpoints": {
            "dashboard": {
                "profile": "/api/dashboard/:username/profile",
                "repositories": "/api/dashboard/:username/repositories",
                "timeline": "/api/dashboard/:username/timeline",
                "similar": "/api/dashboard/:username/similar",
                "export_cv": "/api/dashboard/:username/export-cv"
            },
            "milestones": "/api/milestones/:username",
            "stale_claims": "/api/stale-claims/:owner/:repo",
            "discovery": "/api/discover/:username"
        }
    })

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

# Dashboard endpoints
@app.route('/api/dashboard/<username>/profile')
def dashboard_profile(username):
    try:
        service = MaintainerDashboard(TOKEN)
        data = service.get_profile(username)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/dashboard/<username>/repositories')
def dashboard_repositories(username):
    try:
        service = MaintainerDashboard(TOKEN)
        data = service.get_repositories(username)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/dashboard/<username>/timeline')
def dashboard_timeline(username):
    try:
        service = MaintainerDashboard(TOKEN)
        data = service.get_timeline(username)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/dashboard/<username>/similar')
def dashboard_similar(username):
    try:
        service = MaintainerDashboard(TOKEN)
        data = service.find_similar_maintainers(username)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/dashboard/<username>/export-cv')
def dashboard_export_cv(username):
    try:
        service = MaintainerDashboard(TOKEN)
        data = service.export_cv(username)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Milestones endpoint
@app.route('/api/milestones/<username>')
def milestones(username):
    try:
        service = MilestoneCelebrations(TOKEN)
        data = service.get_milestone_sections(username)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Stale claims endpoint
@app.route('/api/stale-claims/<owner>/<repo>')
def stale_claims(owner, repo):
    try:
        service = CookieLickingDetector(TOKEN)
        limit = request.args.get('limit', 20, type=int)
        data = service.analyze_repository(f"{owner}/{repo}", limit)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Discovery endpoint
@app.route('/api/discover/<username>', methods=['GET', 'POST'])
def discover(username):
    try:
        service = OSSDiscoveryEngine(TOKEN)
        
        if request.method == 'POST':
            body = request.get_json()
            intent = body.get('intent', 'solve_issues')
            query = body.get('query', '')
            filters = body.get('filters', {})
            limit = body.get('limit', 10)
        else:
            intent = request.args.get('intent', 'solve_issues')
            query = request.args.get('query', '')
            limit = int(request.args.get('limit', 10))
            filters = {}
        
        data = service.discover_projects(username, intent, query, filters, limit)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🚀 Unified OSS API")
    print("="*60)
    print("  Running on: http://localhost:5001")
    print("  Health: http://localhost:5001/api/health")
    print("  Docs: http://localhost:5001/")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
