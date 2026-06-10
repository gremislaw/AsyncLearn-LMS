import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_course_as_admin(client: AsyncClient, admin_token: str):
    response = await client.post(
        "/api/v1/courses/",
        json={"title": "Test Course", "description": "Desc", "price": 10.0},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Course"
    assert data["price"] == 10.0

@pytest.mark.asyncio
async def test_create_course_as_student_forbidden(client: AsyncClient, student_token: str):
    response = await client.post(
        "/api/v1/courses/",
        json={"title": "Test Course 2", "price": 0.0},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_courses(client: AsyncClient):
    response = await client.get("/api/v1/courses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_course_by_id(client: AsyncClient, admin_token: str):
    res = await client.post(
        "/api/v1/courses/",
        json={"title": "Fetch Me", "price": 5.0},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    course_id = res.json()["id"]
    
    response = await client.get(f"/api/v1/courses/{course_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Fetch Me"

@pytest.mark.asyncio
async def test_get_nonexistent_course(client: AsyncClient):
    response = await client.get("/api/v1/courses/9999")
    assert response.status_code == 404
