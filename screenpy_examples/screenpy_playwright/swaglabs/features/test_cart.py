from screenpy import given, then, when
from screenpy.actions import SeeAllOf
from screenpy.resolutions import ContainsTheText, IsEqualTo
from screenpy_playwright.actions import Click
from screenpy_playwright.questions import Number, Text

from ..questions import ShoppingCartBadgeNumber
from ..tasks import LogIn
from ..ui.cart_page import CART_ITEMS, FIRST_CART_ITEM
from ..ui.header import CART_ICON
from ..ui.store_page import BACKPACK_ADD_TO_CART_BUTTON
from ..user_types import StandardUser


def test_add_to_cart(Swalter):
    given(Swalter).was_able_to(LogIn.as_(StandardUser))

    when(Swalter).attempts_to(
        Click.on_the(BACKPACK_ADD_TO_CART_BUTTON),
        Click.on_the(CART_ICON),
    )

    then(Swalter).should(
        SeeAllOf.the(
            (ShoppingCartBadgeNumber(), IsEqualTo(1)),
            (Number.of(CART_ITEMS), IsEqualTo(1)),
            (
                Text.of_the(FIRST_CART_ITEM),
                ContainsTheText("Sauce Labs Backpack")
            ),
        )
    )
