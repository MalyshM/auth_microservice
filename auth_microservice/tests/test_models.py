from src.dynamic_models import (
    UserBaseType,
    UserCreateType,
    USERNAME_FIELD,
    EMAIL_FIELD,
    PHONE_FIELD,
    PASSWORD_FIELD,
)
import pytest


def test_user_base_fields():
    assert UserBaseType.model_fields is not None


def test_user_base_with_username():
    user = UserBaseType(**{USERNAME_FIELD: "asd"})
    assert getattr(user, USERNAME_FIELD) == "asd"
    assert user.get_valid_field == (USERNAME_FIELD, "asd")


def test_user_base_with_email():
    user = UserBaseType(**{EMAIL_FIELD: "mama_ya_sozdal_pochty@mail.ru"})
    assert getattr(user, EMAIL_FIELD) == "mama_ya_sozdal_pochty@mail.ru"
    assert user.get_valid_field == (
        EMAIL_FIELD,
        "mama_ya_sozdal_pochty@mail.ru",
    )


def test_user_base_with_phone():
    user = UserBaseType(**{PHONE_FIELD: "+71234567890"})
    assert getattr(user, PHONE_FIELD) == "+71234567890"
    assert user.get_valid_field == (PHONE_FIELD, "+71234567890")


def test_user_base_with_empty_field():
    user = UserBaseType(
        **{USERNAME_FIELD: "asd", EMAIL_FIELD: "", PHONE_FIELD: ""}
    )
    assert getattr(user, USERNAME_FIELD) == "asd"
    assert getattr(user, EMAIL_FIELD) is None
    assert getattr(user, PHONE_FIELD) is None
    assert user.get_valid_field == ("username", "asd")


def test_user_base_with_invalid_email():
    with pytest.raises(ValueError):
        UserBaseType(**{EMAIL_FIELD: "mama_ya_sozdal_pochty@mail"})


def test_user_base_with_invalid_phone1():
    with pytest.raises(ValueError):
        UserBaseType(**{PHONE_FIELD: "71234567890"})


def test_user_base_with_phone2():
    user = UserBaseType(**{PHONE_FIELD: "812345678901"})
    assert getattr(user, PHONE_FIELD) == "81234567890"
    assert user.get_valid_field == (PHONE_FIELD, "81234567890")


def test_user_create_with_username_and_password():
    user_create = UserCreateType(
        **{USERNAME_FIELD: "asd", PASSWORD_FIELD: "asdASD123!@#"}
    )
    assert getattr(user_create, USERNAME_FIELD) == "asd"
    assert getattr(user_create, PASSWORD_FIELD) == "asdASD123!@#"
    assert user_create.get_valid_field == ("username", "asd")


def test_user_create_with_email_and_password():
    user_create = UserCreateType(
        **{
            EMAIL_FIELD: "mama_ya_sozdal_pochty@mail.ru",
            PASSWORD_FIELD: "asdASD123!@#",
        }
    )
    assert getattr(user_create, EMAIL_FIELD) == "mama_ya_sozdal_pochty@mail.ru"
    assert getattr(user_create, PASSWORD_FIELD) == "asdASD123!@#"
    assert user_create.get_valid_field == (
        EMAIL_FIELD,
        "mama_ya_sozdal_pochty@mail.ru",
    )


def test_user_create_with_phone_and_password():
    user_create = UserCreateType(
        **{PHONE_FIELD: "+71234567890", PASSWORD_FIELD: "asdASD123!@#"}
    )
    assert getattr(user_create, PHONE_FIELD) == "+71234567890"
    assert getattr(user_create, PASSWORD_FIELD) == "asdASD123!@#"
    assert user_create.get_valid_field == (PHONE_FIELD, "+71234567890")


def test_user_create_invalid_email():
    with pytest.raises(ValueError):
        UserCreateType(
            **{EMAIL_FIELD: "invalid_email", PASSWORD_FIELD: "asdASD123!@#"}
        )


def test_user_create_no_fields():
    with pytest.raises(ValueError):
        UserCreateType(**{PASSWORD_FIELD: "asdASD123!@#"})


def test_user_create_with_incorrect_password():
    for password in ["as", "asdasdasdasd", "asdasdasd123", "ASDASDASD123"]:
        with pytest.raises(ValueError):
            UserCreateType(**{USERNAME_FIELD: "asd", PASSWORD_FIELD: password})
