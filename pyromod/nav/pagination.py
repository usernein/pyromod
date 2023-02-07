from pyrogram.types import InlineKeyboardButton
from ..helpers import ikb


class Pagination:
    """
     Creates a full paginated menu

    Parameters:
        List: List of your items

        Attach: Pass the empty predefined list, to append items that should be shown.

        Back: Pass your button for returning to previous menu. If empty, default value will be used.
            Default: ("↩️", "callback_data=Back")

        Backward: Pass your button to show previous page. If empty, default value will be used.
            Default: ("⬅️", "callback_data=Backward")

        Forward: Pass your button to show next page. If empty, default value will be used.
            Default: ("➡️", "callback_data=Forward")

        Page: Pass the page number that should be shown.

        row_per_page: Pass the number of rows that each page should have.
    """

    def __init__(self, List: list[list[InlineKeyboardButton]],
                 Attach: list,
                 Back: list[list[InlineKeyboardButton]] = None,
                 Backward: list[list[InlineKeyboardButton]] = None,
                 Forward: list[list[InlineKeyboardButton]] = None,
                 Page: int = 1, row_per_page: int = 4):

        self.__List = List
        self.__Attach = Attach
        self.__row_per_page = row_per_page
        self.__current_page = Page
        self.__Total_page = self.__Total_page()
        self.__Back = Back if isinstance(Back, list) else ikb([("↩️", "Back")], Markup=False)[0]
        self.__Backward = Backward if isinstance(Backward, list) else ikb([("⬅️", "Backward")], Markup=False)[0]
        self.__Forward = Forward if isinstance(Forward, list) else ikb([("➡️", "Forward")], Markup=False)[0]

    def __ikb_move_btns(self):
        if self.__current_page == self.__Total_page and self.__Total_page == 1:
            self.__Attach.extend([self.__Back])

        elif self.__current_page == self.__Total_page and self.__Total_page > 1:
            self.__Attach.extend([self.__Backward])

        elif self.__current_page == 1 and self.__Total_page > self.__current_page:
            self.__Attach.extend([self.__Back + self.__Forward])

        elif self.__Total_page > self.__current_page > 1:
            self.__Attach.extend([self.__Backward + self.__Backward])

    def __create_page(self):
        Start = (self.__current_page - 1) * self.__row_per_page
        End = Start + self.__row_per_page
        self.__Attach.extend(self.__List[Start:End])

    def __Total_page(self):
        Num = len(self.__List)
        return (Num // self.__row_per_page) + (Num % self.__row_per_page > 0)

    def Create(self):
        self.__create_page()
        self.__ikb_move_btns()
