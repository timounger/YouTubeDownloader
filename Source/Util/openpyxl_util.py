"""!
********************************************************************************
@file   openpyxl_util.py
@brief  Util function for openpyxl
********************************************************************************
"""

from typing import Optional
from datetime import datetime, time
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet import table
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.styles.borders import Border, Side


FONT_SIZE = 11
FONT_NAME = "Calibri"
MAX_COLUMN_WIDTH = 30
MAX_ROW_HEIGHT = 1.3

# https://www.farb-tabelle.de/de/farbtabelle.htm
COLOR_BLACK = "000000"
COLOR_BLUE = "0000FF"
COLOR_BROWN = "A52A2A"
COLOR_GREY = "BEBEBE"
COLOR_GREEN = "00FF00"
COLOR_ORANGE = "FFA500"
COLOR_RED = "FF0000"
COLOR_VIOLET = "EE82EE"
COLOR_WHITE = "FFFFFF"
COLOR_YELLOW = "FFFF00"

THIN_BORDER = Border(left=Side(style="thin"),
                     right=Side(style="thin"),
                     top=Side(style="thin"),
                     bottom=Side(style="thin"))

NUMBER_FORAMT_CURRENCY = "#,##0.00"
NUMBER_FORMAT_EUR = "#,##0.00 €"
NUMBER_FORMAT_PERCENT = "0%"
NUMBER_FORMAT_DATETIME = "YYYY-MM-DD HH:MM:SS"
NUMBER_FORMAT_TIME = "hh:mm"

PAGE_MARGIN_FACTOR = 1 / 2.54  # convert inch to cm


class XLSCreator():
    """!
    @brief XLS file creator
    @param font_name : default font name
    @param font_size : default font size
    """

    def __init__(self, font_name: Optional[str] = None, font_size: Optional[int] = None):
        self.font_name = FONT_NAME if (font_name is None) else font_name
        self.font_size = FONT_SIZE if (font_size is None) else font_size
        self.workbook = Workbook()

    def save(self, filename: str) -> None:
        """!
        @brief Save file
        @param filename : name of file
        """
        self.workbook.save(filename=filename)

    def set_table(self, worksheet: Worksheet, max_col: int, max_row: int, min_col: int = 1, min_row: int = 1) -> None:
        """!
        @brief Set table
        @param worksheet : worksheet
        @param max_col : maximum column
        @param max_row : maximum row
        @param min_col : minimum column (default is first column)
        @param min_row : worksheet (default is first row)
        """
        table_style = table.TableStyleInfo(name="TableStyleLight15",
                                           showRowStripes=True)
        start_cell = get_column_letter(min_col) + str(min_row)
        end_cell = get_column_letter(max_col) + str(max_row)
        new_table = table.Table(ref=f"{start_cell}:{end_cell}",
                                displayName=worksheet.title,
                                tableStyleInfo=table_style)
        worksheet.add_table(new_table)

    def set_page_marcins(self, worksheet: Worksheet, left: Optional[float] = None, right: Optional[float] = None,
                         top: Optional[float] = None, bottom: Optional[float] = None) -> None:
        """!
        @brief Set page margins in cm
        @param worksheet : select worksheet
        @param left : left margin in cm
        @param right : left margin in cm
        @param top : left margin in cm
        @param bottom : left margin in cm
        """
        if left is not None:
            worksheet.page_margins.left = left * PAGE_MARGIN_FACTOR
        if right is not None:
            worksheet.page_margins.right = right * PAGE_MARGIN_FACTOR
        if top is not None:
            worksheet.page_margins.top = top * PAGE_MARGIN_FACTOR
        if bottom is not None:
            worksheet.page_margins.bottom = bottom * PAGE_MARGIN_FACTOR

    def set_column_autowidth(self, worksheet: Worksheet, b_limit: bool = True) -> None:
        """!
        @brief Set automatic column width of worksheet.
        @param worksheet : select worksheet
        @param b_limit : status if width has a max limit
        """
        for i, col_cells in enumerate(worksheet.columns, start=1):
            i_max_col_len = 0
            for j, cell in enumerate(col_cells):
                if b_limit:
                    if j != 0:  # do use not use first line description
                        i_max_col_len = max(i_max_col_len, len(str(cell.value).split("n", maxsplit=1)[0]))
                else:
                    for s_line in str(cell.value).split("/n"):
                        i_max_col_len = max(i_max_col_len, len(s_line))
            if b_limit:
                i_max_col_len = min(i_max_col_len, MAX_COLUMN_WIDTH)
            if i_max_col_len == 0:
                worksheet.column_dimensions[get_column_letter(i)].hidden = True  # hide empty lines
            else:
                worksheet.column_dimensions[get_column_letter(i)].width = (i_max_col_len + 1) * 0.10 * self.font_size

    def set_row_autoheight(self, worksheet: Worksheet, b_limit: bool = True) -> None:
        """!
        @brief Set automatic row height of worksheet.
        @param worksheet : select worksheet
        @param b_limit : status if height has a max limit
        """
        for i, col_cells in enumerate(worksheet.rows, start=1):
            i_high = MAX_ROW_HEIGHT
            if not b_limit:
                for cell in col_cells:
                    i_high = max(i_high, len(str(cell.value).split("\n")) * MAX_ROW_HEIGHT)
            worksheet.row_dimensions[i].height = i_high * self.font_size

    def set_cell(self, ws: Worksheet, row: int, column: int, value: Optional[str | int | float | datetime | time] = None,
                 font_name: Optional[str] = None, color: Optional[str] = None, font_size: Optional[int] = None,
                 bold: bool = False, italic: bool = False, strike: bool = False, underline: Optional[str] = None,
                 vert_align: Optional[str] = None, fill_color: Optional[str] = None,
                 align: Optional[str] = None, align_vert: Optional[str] = "center", wrap_text: bool = False,
                 number_format: Optional[str] = None, border: Optional[Border] = None) -> None:
        """!
        @brief Set cell data
               Font: https://openpyxl.readthedocs.io/en/stable/api/openpyxl.styles.fonts.html
               PatternFill: https://openpyxl.readthedocs.io/en/stable/api/openpyxl.styles.fills.html#openpyxl.styles.fills.PatternFill
               Alignment: https://openpyxl.readthedocs.io/en/latest/api/openpyxl.styles.alignment.html
        @param ws : worksheet
        @param row : row position
        @param column : column position
        @param value : cell value [numeric, time, string, bool, None]
        @param font_name : font name (default is Calibri)
        @param color : font color e.g. "FF0000" for red
        @param font_size : font size
        @param bold : status if cell content should be bold
        @param italic : status if cell content should be italic
        @param strike : strike option
        @param underline : underline options ['double', 'doubleAccounting', 'single', 'singleAccounting']
        @param vert_align : vertical align options ['superscript', 'subscript', 'baseline']
        @param fill_color : background fill color of cell
        @param align : horizontal text align option ["general", "left", "center", "right", "fill", "justify", "centerContinuous", "distributed"]
        @param align_vert : vertical text align of cell ["top", "center", "bottom", "justify", "distributed"]
        @param wrap_text : wrap text
        @param number_format : number format of cell
        @param border : border of cell
        """
        if font_name is None:
            font_name = self.font_name
        if font_size is None:
            font_size = self.font_size
        cell = ws.cell(row=row, column=column, value=value)
        cell.font = Font(name=font_name, color=color, size=str(font_size), bold=bold, italic=italic,
                         strikethrough=strike, underline=underline, vertAlign=vert_align)
        if fill_color is not None:
            cell.fill = PatternFill(fill_type="solid", start_color=fill_color, end_color=fill_color)
        cell.alignment = Alignment(horizontal=align, vertical=align_vert, wrap_text=wrap_text)
        if number_format is not None:
            cell.number_format = number_format
        if border is not None:
            cell.border = border
