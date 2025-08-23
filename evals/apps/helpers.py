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
