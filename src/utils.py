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
