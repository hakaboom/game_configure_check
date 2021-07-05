from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font, NamedStyle

__all__ = ['xlStyle']


xlStyle = NamedStyle(name='xlStyle')
_thin = Side(border_style='thin', color='000000')
xlStyle.border = Border(left=_thin, top=_thin, right=_thin, bottom=_thin)
xlStyle.alignment = Alignment(horizontal='center', vertical='center')

