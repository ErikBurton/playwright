def test_homepage_is_reachable(api_context):
    response = api_context.get("/")

    assert response.status == 200
    assert "The Internet" in response.text()
