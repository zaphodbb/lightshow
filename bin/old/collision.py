# SPDX-FileCopyrightText: 2020 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`collision`
================================================================================

Comet collision animation for CircuitPython helper library for LED animations.

* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


"""

from adafruit_led_animation.animation import Animation
from adafruit_led_animation.color import BLACK, calculate_intensity


class Collision(Animation):
    """
    A comet collision animation.

    :param pixel_object: The initialised LED object.
    :param float speed: Animation speed in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    :param int tail_length: The length of the comet. Defaults to 25% of the length of the
                            ``pixel_object``. Automatically compensates for a minimum of 2 and a
                            maximum of the length of the ``pixel_object``.
    :param int skip: Pixels to skip with each refresh.  Defaults to 0.
    :param excolor: Explosion color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    """

    # pylint: disable=too-many-arguments,too-many-instance-attributes
    def __init__(
        self,
        pixel_object,
        speed,
        color,
        tail_length=0,
        name=None,
        skip=0,
        excolor,
    ):
        if tail_length == 0:
            tail_length = len(pixel_object) // 4
        self._tail_length = tail_length
        self._color_step = 0.95 / tail_length
        self._left_comet_colors = None
        self._right_comet_colors = None
        self._explosion_colors = None
        self._computed_color = color
        self._num_pixels = len(pixel_object)
        self._direction = -1 if reverse else 1
        self._left_side = -self._tail_length
        self._center = int(self._num_pixels / 2)
        self._right_side = self._num_pixels + self._tail_length
        self._tail_start = 0
        self._skip = skip
        self._skipval = skip
        self._excolor = excolor
        self.reset()
        super().__init__(pixel_object, speed, color, name=name)

    on_cycle_complete_supported = True

    def _set_color(self, color):
        self._right_comet_colors = [BLACK]
        for n in range(self._tail_length):
            self._right_comet_colors.append(
                calculate_intensity(color, n * self._color_step + 0.05)
            )
        self._left_comet_colors = reversed(self._right_comet_colors)
        self._computed_color = color

    def draw(self):
        colors = self._comet_colors
        if self.reverse:
            colors = reversed(colors)

        for pixel_no in range(self._skipval):
            if self._reverse:
                draw_at = self._tail_start + self._tail_length + pixel_no + 1
            else:
                draw_at = self._tail_start - pixel_no - 1
            if draw_at < 0 or draw_at >= self._num_pixels:
                continue
            self.pixel_object[draw_at] = BLACK

        for pixel_no, color in enumerate(colors):
            draw_at = self._tail_start + pixel_no 
            if draw_at < 0 or draw_at >= self._num_pixels:
                if not self._ring:
                    continue
                draw_at = draw_at % self._num_pixels

            self.pixel_object[draw_at] = color

        self._tail_start += (self._direction + self._skip)

        if self._tail_start < self._left_side or (
            self._tail_start >= self._right_side and not self._reverse
        ):
            if self.bounce:
                self.reverse = not self.reverse
            elif self._ring:
                self._tail_start = self._tail_start % self._num_pixels
            else:
                self.reset()

            self.cycle_complete = True

    def reset(self):
        """
        Resets to the first state.
        """
        junk = 1
