# pyLiveKML: A python library that streams geospatial data using the KML protocol.
# Copyright (C) 2022 smoke-you

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Helpers module for the eval server."""


def description_builder(src: dict, title_color: int = 0xFF0000) -> str:
    """Transform a dict that describes a KML object into a formatted HTML table.

    :param dict src: The dict that will be used to build the description.
    :param int title_color: The color that will be used to display the title column.
    :return: The description as an HTML-formatted table.
    :rtype: str
    """
    if not src:
        return "<table />"
    rows = ["<table>"]
    title_color = title_color & 0xFFFFFF
    for k, v in src.items():
        if isinstance(v, (tuple, list)):
            row = [
                f'<tr><td align="left" style="color:#{title_color:06x}"><b>{k}</b></td>'
            ]
            for i in v:
                row.append(f'<td align="right">{str(i)}</td>')
            row.append("</tr>")
            rows.append("".join(row))
        else:
            rows.append(
                f'<tr><td align="left" style="color:#{title_color:06x}"><b>{k}</b></td>'
                f'<td align="right">{str(v)}</td></tr>'
            )
    rows.append("</table>")
    return "".join(rows)
