
def test_health(client) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200


def test_sample_assessment(client) -> None:
    response = client.post("/api/cutover/sample/core_cutover_plan")
    assert response.status_code == 200
    body = response.json()
    assert body["report"]["decision"] in {"GO", "CAUTION", "HOLD"}


def test_history_page(client) -> None:
    client.post("/api/cutover/sample/core_cutover_plan")
    response = client.get("/history")
    assert response.status_code == 200
