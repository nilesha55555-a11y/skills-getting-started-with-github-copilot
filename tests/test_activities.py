from urllib.parse import quote


def test_get_activities_returns_seed_data(client):
    # Arrange
    # No setup needed; the app starts with seeded activities.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity_registers_student(client):
    # Arrange
    activity_name = "Chess Club"
    student_email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup?email={quote(student_email)}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {student_email} for {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert student_email in activity["participants"]


def test_signup_for_duplicate_email_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup?email={quote(existing_email)}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_removes_email(client):
    # Arrange
    activity_name = "Chess Club"
    student_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/unregister?email={quote(student_email)}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {student_email} from {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert student_email not in activity["participants"]


def test_unregister_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Activity"
    student_email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/unregister?email={quote(student_email)}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    student_email = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/unregister?email={quote(student_email)}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"
