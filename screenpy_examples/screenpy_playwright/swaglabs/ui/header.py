from __future__ import annotations

from screenpy_playwright import Target

CART_ICON = Target.the("cart icon").located_by("#shopping_cart_container")
CART_BADGE = Target.the("cart items badge").located_by("span.shopping_cart_badge")
