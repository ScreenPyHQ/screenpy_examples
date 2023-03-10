from screenpy import Actor
from screenpy.pacing import beat
from screenpy_playwright.questions import Text

from screenpy_examples.screenpy_playwright.swaglabs.ui.header import CART_BADGE


class ShoppingCartBadgeNumber:
    """Get the number in the badge on the shopping cart icon.

    Examples::

        the_actor.should(See.the(ShoppingCartBadgeNumber(), IsEqualTo(903)))
    """

    @beat("{} reads the number of items in their shopping cart.")
    def answered_by(self, the_actor: Actor) -> int:
        """Direct the actor to ask about the number of items in their cart."""
        return int(Text.of_the(CART_BADGE).answered_by(the_actor))
