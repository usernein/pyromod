### *class* pyromod.nav.Pagination

The `pyromod.nav.Pagination` class provides a utility for creating paginated interfaces with customizable pagination
controls. It is designed to handle a list of objects and display them in a paginated manner.

### *Parameters:*

- **objects** (*list*) – The list of items to paginate.
- **page_data** (*function*) – A function to customize the data displayed in the pagination controls for each page. The
  default function returns the page number as a string.
- **item_data** (*function*) – A function to customize the data displayed for each item in the pagination. The default
  function prefixes each item with the page number.
- **item_title** (*function*) – A function to customize the title displayed for each item. The default function prefixes
  each item with the page number in square brackets.

### *create(page, lines=5, columns=1)*

Creates a paginated interface for the specified page.

**Parameters:**

- **page** (*int*) – The page number to display.
- **lines** (*int*) – The number of lines (rows) per page.
- **columns** (*int*) – The number of columns per page.

**Returns:**
A list of paginated items and pagination controls in the form of button data.
