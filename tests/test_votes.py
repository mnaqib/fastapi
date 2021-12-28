def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[1].id, "dir": 1})

    print(res.json())
    assert res.status_code == 201


def test_unauthorized_vote_on_post(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[1].id, "dir": 1})

    print(res.json())
    assert res.status_code == 401


def test_delete_vote_on_post(authorized_client, test_posts, test_votes):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})

    print(res.json())
    assert res.status_code == 201


def test_vote_on_post_already_voted(authorized_client, test_votes, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})

    print(res.json())
    assert res.status_code == 409


def test_delete_vote_does_not_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})

    print(res.json())
    assert res.status_code == 404


def test_vote_on_post_not_exist(authorized_client):
    res = authorized_client.post("/vote/", json={"post_id": 1107, "dir": 1})

    print(res.json())
    assert res.status_code == 404
