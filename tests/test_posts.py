from app import schema
import pytest


def test_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    posts = res.json()
    for post in posts:
        get_post = schema.PostOut(**post)
    assert len(posts) == len(test_posts)
    assert res.status_code == 200


def test_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    post = schema.PostOut(**res.json())
    assert post.title == test_posts[0].title
    assert res.status_code == 200


def test_get_one_post_not_exist(client, test_posts):
    res = client.get("/posts/1107")
    assert res.status_code == 404


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("new_post 1", "1st post content", True),
        ("new_post 2", "2nd post content", True),
        ("new_post 3", "3rd post content", False),
    ],
)
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        "/posts/",
        json={
            "title": title,
            "content": content,
            "published": published,
        },
    )

    post = schema.Post(**res.json())

    assert res.status_code == 201
    assert post.title == title
    assert post.owner.id == test_user["id"]


def test_create_post_default_publish(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/",
        json={
            "title": "last post",
            "content": "some content",
        },
    )

    post = schema.Post(**res.json())

    assert res.status_code == 201
    assert post.owner.id == test_user["id"]


def test_unauthorized_create_post(client):
    res = client.post(
        "/posts/",
        json={
            "title": "last post",
            "content": "some content",
        },
    )
    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[1].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client):
    res = authorized_client.delete(f"/posts/1107")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    res = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json={
            "title": "updates post",
            "content": test_posts[0].content,
            "published": False,
        },
    )

    updated_post = schema.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.owner.id == test_posts[0].owner.id


def test_unauthorized_update_post(client, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}",
        json={
            "title": "updates post",
            "content": test_posts[0].content,
            "published": False,
        },
    )

    assert res.status_code == 401


def test_update_other_user_post(authorized_client, test_posts):
    res = authorized_client.put(
        f"/posts/{test_posts[3].id}",
        json={
            "title": "updates post",
            "content": test_posts[3].content,
            "published": False,
        },
    )

    assert res.status_code == 403


def test_update_post_non_exist(authorized_client, test_posts):
    res = authorized_client.put(
        f"/posts/1107",
        json={
            "title": "updates post",
            "content": test_posts[0].content,
            "published": False,
        },
    )
    assert res.status_code == 404
