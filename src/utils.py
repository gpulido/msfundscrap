def sanitize_text(text):
    """Basic cleanning text helper. Remove trailing and ending spaces and '\n' chars
    Can be improved if needed

    Args:
        text (str): the string to sanitize

    Returns:
        str: the string sanitized
    """
    return text.replace('\n', '').strip()

def read_float_with_comma(num):
    """Helper method to parse a float string representation that has
    a comma as decimal separator.
    Can't use locale as the page being parsed could not be in the 
    same locale as the python running environment

    Args:
        num (str): the float string to parse

    Returns:
        float: the parsed float
    """
    return float(num.replace(",", "."))
    
def number_from_class(number_class):
    """Helper method to return the last char as integer from a numbered
    class. example: stars1 stars2 stars3

    Args:
        number_class (str): class name that has a number at the end

    Returns:
        int: the number representation of the class.
    """
    return int(number_class[-1])


def parse_table(table, header_class, value_class):    
    """Parses a TR / TD table from MS 
    TODO: move to the utils

    Args:
        table (soup table): Soup table loaded from MS
        header_class(str): the name of the css class that identifies header columns
        value_class(str): the name of the css class that identifies value columns

    Returns:
        [dictionary]: dictionary with the values of the table
    """
    values = {}    
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        name = ''
        value = ''
        for column in columns:            
            # if not 'line' in column.attrs['class']:
            #     continue
            if header_class in column.attrs['class']:
                name = column.get_text()
            elif value_class in column.attrs['class']:
                value = column.get_text()
        if name != '' and value != '':
            values[name] = value
    return values

