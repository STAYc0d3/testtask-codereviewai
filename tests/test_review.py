import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_review_code():
    response = client.post("/api/v1/review", json={
        "assignment_description": "Analyze this code for best practices.",
        "github_repo_url": "https://github.com/STAYc0d3/Todoapp",
        "candidate_level": "Junior"
    })
    print("\n=== Response from API ===")
    print(response.json())
    print("=======================")
    assert response.status_code == 200
    assert "content" in response.json()

def test_review_code_invalid_level():
    response = client.post("/api/v1/review", json={
        "assignment_description": "Analyze this code for best practices.",
        "github_repo_url": "https://github.com/STAYc0d3/Todoapp",
        "candidate_level": "Invalid"  # неправильний рівень
    })
    print("\n=== Invalid Level Response ===")
    print(response.json())
    print("============================")
    assert response.status_code == 422

def test_review_code_invalid_url():
    response = client.post("/api/v1/review", json={
        "assignment_description": "Analyze this code for best practices.",
        "github_repo_url": "invalid-url",  # неправильний URL
        "candidate_level": "Junior"
    })
    print("\n=== Invalid URL Response ===")
    print(response.json())
    print("==========================")
    assert response.status_code == 422

def test_review_code_empty_description():
    response = client.post("/api/v1/review", json={
        "assignment_description": "",  # пустий опис
        "github_repo_url": "https://github.com/STAYc0d3/Todoapp",
        "candidate_level": "Junior"
    })
    print("\n=== Empty Description Response ===")
    print(response.json())
    print("===============================")
    assert response.status_code == 422
