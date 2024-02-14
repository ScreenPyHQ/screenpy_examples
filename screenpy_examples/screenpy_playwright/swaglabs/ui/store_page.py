from __future__ import annotations

from screenpy_playwright import Target

BACKPACK_ADD_TO_CART_BUTTON = Target.the('backpack\'s "Add To Cart" button').located_by(
    "#add-to-cart-sauce-labs-backpack"
)
