from __future__ import annotations

from screenpy_playwright import Target

CART_ITEMS = Target.the("cart items").located_by("div.cart_item")
FIRST_CART_ITEM = Target.the("first cart item").located_by("div.cart_item >> nth=0")
