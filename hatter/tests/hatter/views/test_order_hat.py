from django.contrib.auth.models import User
import pytest


@pytest.mark.django_db
@pytest.fixture
def a_user():
    return User.objects.create_user(username="cold-person", password="im-a-freezin")


@pytest.mark.django_db
def test_order_hat(client, a_user):
    _ = a_user  # kill unused warning

    resp = client.post(
        "/hat/order",
        content_type="application/json",
        headers={"Authorization": "Basic Y29sZC1wZXJzb246aW0tYS1mcmVlemlu"},
        data={
            "colour": "white",
            "material": "wool",
            "order_number": 27,
        },
    )
    assert resp.status_code == 200
    assert resp.data == {
        "customer": "cold-person",
        "colour": "white",
        "material": "wool",
        "order_number": 27,
    }
