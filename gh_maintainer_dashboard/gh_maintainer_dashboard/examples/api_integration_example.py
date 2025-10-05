"""
API integration example - How to use the module with FastAPI
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from gh_maintainer_dashboard import MaintainerDashboard
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Maintainer Dashboard API")

github_token = os.getenv("GITHUB_TOKEN")
dashboard = MaintainerDashboard(github_token=github_token)


@app.get("/")
async def root():
    return {"message": "Maintainer Dashboard API", "version": "0.1.0"}


@app.get("/api/maintainer/{username}")
async def get_maintainer_profile(username: str):
    try:
        profile = dashboard.get_profile(username)
        return JSONResponse(content=profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/maintainer/{username}/cv")
async def get_maintainer_cv(username: str, format: str = "json"):
    try:
        cv = dashboard.export_cv(username, format=format)
        return JSONResponse(content=cv)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/maintainer/{username}/similar")
async def get_similar_maintainers(username: str, limit: int = 10):
    try:
        similar = dashboard.find_similar_maintainers(username, limit)
        return JSONResponse(content={"similar_maintainers": similar})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/maintainer/{username}/repos")
async def get_maintainer_repos(username: str):
    try:
        repos = dashboard.get_repositories(username)
        return JSONResponse(content=repos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/maintainer/{username}/timeline")
async def get_maintainer_timeline(username: str, period: str = "30d"):
    try:
        timeline = dashboard.get_timeline(username, period)
        return JSONResponse(content=timeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
