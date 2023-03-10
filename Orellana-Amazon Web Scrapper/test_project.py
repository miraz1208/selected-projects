"""
This test file collectively tests implementations of
validate_product_name, page_start_end, and get_url functions of project.py
thoroughly.
"""
from unittest import mock  # To initiate mock input for input function
from project import validate_product_name, page_start_end, get_url


@mock.patch('project.input')
def test_validate_product_name(mocked_input):
    """
    Tests validate_product_name function of project.py
    """

    # Test correct entry
    mocked_input.side_effect = ['Tea']
    test = validate_product_name()
    assert test == 'tea'

    # Test misspelled entry
    mocked_input.side_effect = ['Cofee', 'Y', 'coffee']
    test = validate_product_name()
    assert test == 'coffee'

    # Test all int entry
    mocked_input.side_effect = ['1234', '5gum']
    test = validate_product_name()
    assert test == '5gum'


@mock.patch('project.input')
def test_page_start_end(mocked_input):
    """
    Tests page_start_end function of project.py
    """
    # Test correct entry
    mocked_input.side_effect = ['1', '5']
    test = page_start_end()
    assert test == (1, 5)

    # Test start at page '0' entry
    mocked_input.side_effect = ['0', '1', '2']
    test = page_start_end()
    assert test == (1, 2)

    # Test valid start page but invalid end page entry
    mocked_input.side_effect = ['3', '1', '5']
    test = page_start_end()
    assert test == (3, 5)

    # Test invalid start page entry
    mocked_input.side_effect = ['a', '1', '5']
    test = page_start_end()
    assert test == (1, 5)


def test_get_url():
    """
    Tests get_url function of project.py
    """
    assert get_url(
        'gum') == 'https://www.amazon.com/s?k=gum&ref=nb_sb_noss&page={}'
