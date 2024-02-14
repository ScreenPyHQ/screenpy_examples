from __future__ import annotations

from screenpy import Actor, ContainsTheText, IsEqualTo, SeeAllOf, given, then, when
from screenpy_playwright.actions import Click
from screenpy_playwright.questions import Number, Text

from screenpy_examples.screenpy_playwright.swaglabs.questions import (
    ShoppingCartBadgeNumber,
)
from screenpy_examples.screenpy_playwright.swaglabs.tasks import LogIn
from screenpy_examples.screenpy_playwright.swaglabs.ui.cart_page import (
    CART_ITEMS,
    FIRST_CART_ITEM,
)
from screenpy_examples.screenpy_playwright.swaglabs.ui.header import CART_ICON
from screenpy_examples.screenpy_playwright.swaglabs.ui.store_page import (
    BACKPACK_ADD_TO_CART_BUTTON,
)
from screenpy_examples.screenpy_playwright.swaglabs.user_types import StandardUser


def test_add_to_cart(Swalter: Actor) -> None:
    given(Swalter).was_able_to(LogIn.as_(StandardUser))

    when(Swalter).attempts_to(
        Click.on_the(BACKPACK_ADD_TO_CART_BUTTON),
        Click.on_the(CART_ICON),
    )

    then(Swalter).should(
        SeeAllOf.the(
            (ShoppingCartBadgeNumber(), IsEqualTo(1)),
            (Number.of(CART_ITEMS), IsEqualTo(1)),
            (Text.of_the(FIRST_CART_ITEM), ContainsTheText("Sauce Labs Backpack")),
        )
    )
