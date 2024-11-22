from src.models import UserBase, UserCreate
import pytest


def test_user_base_fields():
    assert UserBase.model_fields is not None


def test_user_base_with_username():
    user = UserBase(username="asd")
    assert user.username == "asd"
    assert user.get_valid_field == ("username", "asd")


def test_user_base_with_email():
    user = UserBase(email="mama_ya_sozdal_pochty@mail.ru")
    assert user.email == "mama_ya_sozdal_pochty@mail.ru"
    assert user.get_valid_field == ("email", "mama_ya_sozdal_pochty@mail.ru")


def test_user_base_with_invalid_email():
    with pytest.raises(ValueError):
        UserBase(email="mama_ya_sozdal_pochty@mail")


def test_user_base_with_phone():
    user = UserBase(phone="+71234567890")
    assert user.phone == "+71234567890"
    assert user.get_valid_field == ("phone", "+71234567890")


def test_user_base_with_invalid_phone1():
    with pytest.raises(ValueError):
        UserBase(phone="71234567890")


def test_user_base_with_phone2():
    user = UserBase(phone="812345678901")
    assert user.phone == "81234567890"
    assert user.get_valid_field == ("phone", "81234567890")


def test_user_create_with_username_and_incorrect_password():
    with pytest.raises(ValueError):
        UserCreate(username="asd", password="as")


def test_user_create_with_username_and_incorrect_password1():
    with pytest.raises(ValueError):
        UserCreate(username="asd", password="asdasdasdasd")


def test_user_create_with_username_and_incorrect_password2():
    with pytest.raises(ValueError):
        UserCreate(username="asd", password="asdasdasd123")


def test_user_create_with_username_and_incorrect_password3():
    with pytest.raises(ValueError):
        UserCreate(username="asd", password="ASDASDASD123")


def test_user_create_with_username_and_password():
    user_create = UserCreate(username="asd", password="asdASD123!@#")
    assert user_create.username == "asd"
    assert user_create.password == "asdASD123!@#"
    assert user_create.get_valid_field == ("username", "asd")


def test_user_create_with_email_and_password():
    user_create = UserCreate(
        email="mama_ya_sozdal_pochty@mail.ru", password="asdASD123!@#"
    )
    assert user_create.email == "mama_ya_sozdal_pochty@mail.ru"
    assert user_create.password == "asdASD123!@#"
    assert user_create.get_valid_field == (
        "email",
        "mama_ya_sozdal_pochty@mail.ru",
    )


def test_user_create_with_phone_and_password():
    user_create = UserCreate(phone="+71234567890", password="asdASD123!@#")
    assert user_create.phone == "+71234567890"
    assert user_create.password == "asdASD123!@#"
    assert user_create.get_valid_field == ("phone", "+71234567890")


def test_user_create_invalid_email():
    with pytest.raises(ValueError):
        UserCreate(email="invalid_email", password="asdASD123!@#")


def test_user_create_no_fields():
    with pytest.raises(ValueError):
        UserCreate(password="asdASD123!@#")
