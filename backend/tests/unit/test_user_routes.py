def test_get_profile(client, mock_user):
    response = client.get("/profile")
    assert response.status_code == 200
    profile = response.json()
    assert profile["username"] == mock_user.username
    assert profile["email"] == mock_user.email
    assert profile["full_name"] == mock_user.full_name
    assert profile["profile_version"] == mock_user.profile_version


def test_update_profile(client, mock_user):
    payload = {
        "full_name": "Updated User",
        "bio": "Updated bio description",
    }
    response = client.put("/profile", json=payload)
    assert response.status_code == 200
    updated_profile = response.json()
    assert updated_profile["full_name"] == "Updated User"
    assert updated_profile["bio"] == "Updated bio description"
    assert updated_profile["profile_version"] == mock_user.profile_version + 1


def test_deactivate_account(client, mock_user):
    response = client.put("/deactivate")
    assert response.status_code == 200
    assert response.json()["message"] == "Account deactivated successfully"


def test_reactivate_account(client, mock_user):
    mock_user.is_active = False
    response = client.put(f"/reactivate?user_id={mock_user.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Account reactivated successfully"
