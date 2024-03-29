# Copyright (C) 2023 Spencer Magnusson
# semagnum@gmail.com
# Created by Spencer Magnusson
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


def format_round(num: int, division_amount: float) -> str:
    """Formats an integer to a smaller rounded number as a string.

    - format(5432, 1000) = '5'
    - format(5987, 1000) = '6'

    :param num: integer to be
    :param division_amount: dividend
    """
    return str(int(round(num / division_amount, 1)))


def format_num(num: int) -> str:
    """Formats whole numbers to a shorter string representation.

    1,000,000,000 becomes "1B". 1,000,000 becomes "1M". 2,000 becomes "2k". Any smaller number remains as is.

    :param num: number to be simplified.
    """
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return format_round(num, 1000.0) + 'k'
    elif num < 1000000000:
        return format_round(num, 1000000.0) + 'M'
    return format_round(num, 1000000000.0) + 'B'
