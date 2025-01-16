from github import Github, Auth, RateLimitExceededException
from app.core.config import get_settings
import time
import logging
from fastapi import HTTPException

class GitHubService:
    def __init__(self):
        self.settings = get_settings()
        auth = Auth.Token(self.settings.GITHUB_TOKEN)
        self.github = Github(auth=auth)

    async def get_repo_contents(self, repo_url: str):
        try:
            repo_name = repo_url.split("github.com/")[-1].strip()
            repo = self.github.get_repo(repo_name)
            return await self._get_all_contents(repo)
        except RateLimitExceededException:
            # Чекаємо годину перед повторною спробою
            time.sleep(3600)
            return await self.get_repo_contents(repo_url)

    async def _get_all_contents(self, repo, path=""):
        contents = []
        try:
            items = repo.get_contents(path)
            while items:
                file_content = items.pop(0)
                if file_content.type == "dir":
                    items.extend(repo.get_contents(file_content.path))
                else:
                    contents.append(file_content)
        except Exception as e:
            logging.error(f"Error getting repo contents: {str(e)}")
            raise HTTPException(status_code=500, detail="Error accessing repository")
        return contents
