from datetime import datetime
import pandas as pd
from unittest.mock import patch
from project import get_genre, get_episode_range, get_anime_recommendations, anime_recommendation_table, anime_description, get_user_feedback

#Define a helper function that will create a sample DataFrame
def mock_df():
    mock_data = {
    'title': ['Naruto', 'Spy x Family', 'Your Lie in April', 'Violet Evergarden'],
    'genre': ['Action, Adventure, Fantasy', 'Action, Comedy', 'Drama, Romance', 'Drama'],
    'episode_range': ['Very Long', 'Long', 'Medium', 'Short'],
    'description': ['Naruto description', 'Spy x Family description', 'Your Lie in April description', 'Violet Evergarden description'],
    'disclaimer': ['Naruto disclaimer', 'Spy x Family disclaimer', 'Your Lie in April disclaimer', 'Violet Evergarden disclaimer']
    }

    return pd.DataFrame(mock_data)


# ******************************************************************************************************************************************************
#                                                       TEST CASE 1: test_get_genre
# ******************************************************************************************************************************************************

# Test case for valid input
def test_get_genre_valid_choice():
    # Create a mock DataFrame
    df = mock_df()

    # Simulate user input for genre selection (e.g., choosing genre 1 - "Action")
    with patch('builtins.input', return_value = '1'):
        genre = get_genre(df)

    # Assert that the genre returned by the function is the expected one
    assert genre == 'Action'

# Test case for invalid input (e.g., choosing an invalid number)
def test_get_genre_invalid_choice():
    # Create a mock DataFrame
    df = mock_df()

    # Simulate user input where user enters an invalid number ('5')
    with patch('builtins.input', side_effect=['8', '1']):
        genre = get_genre(df)

    # Assert that the function returns the correct genre after retrying the input
    assert genre == 'Action'
    #----------------------------------------------------------------------------
    # Simulate user input where user enters a non-numeric value ('abc')
    with patch('builtins.input', side_effect=['abc', '1']):
        genre = get_genre(df)

    # Assert that the function returns the correct genre after retrying the input
    assert genre == 'Action'

    #----------------------------------------------------------------------------
    # Simulate user input where user enters empty value ('')
    with patch('builtins.input', side_effect=['', '1']):
        genre = get_genre(df)

    # Assert that the function returns the correct genre after retrying the input
    assert genre == 'Action'


# ******************************************************************************************************************************************************
#                                                       TEST CASE 2: test_get_episode_range
# ******************************************************************************************************************************************************

# Test case for valid episode range selection
def test_get_episode_range_valid_choice():
    # Create a mock DataFrame
    df = mock_df()
    # Test with 'Action' genre
    genre =  'Action'

    # Simulate user input where user selects a valid episode range ('4' for Very Long)
    with patch('builtins.input', return_value= '4'):
        episode_range = get_episode_range(df, genre)  # Using 'Action' genre

    # Assert that the function returns the correct episode range
    assert episode_range == 'Very Long'

    #---------------------------------------------------------------------------------------
    # Simulate user input with multiple episode ranges for the 'Action' genre ('3' for Long)
    with patch('builtins.input', return_value= '3'):
        episode_range = get_episode_range(df, genre)

    # Assert that the function returns the correct episode range
    assert episode_range == 'Long'

# Test case for invalid episode range selection
def test_get_episode_range_invalid_choice():
    # Create a mock DataFrame
    df = mock_df()

    # Test with 'Action' genre
    genre =  'Action'

    # Simulate user input where user enters an invalid number ('5') then a valid choice ('1')
    with patch('builtins.input', side_effect=['5', '4']):
        episode_range = get_episode_range(df, genre)  # Using 'Action' genre

    # Assert that the function returns the correct episode range after retrying the input
    assert episode_range == 'Very Long'

    #---------------------------------------------------------------------------------------
    # Simulate user input where user enters empty value and then a valid choice ('1')
    with patch('builtins.input', side_effect=['', '4']):
        episode_range = get_episode_range(df, genre)  # Using 'Action' genre

    # Assert that the function returns the correct episode range after retrying the input
    assert episode_range == 'Very Long'


# ******************************************************************************************************************************************************
#                                                       TEST CASE 3: test_get_anime_recommendations
# ******************************************************************************************************************************************************

# Test case for get_anime_recommendations function
def test_get_anime_recommendations_results():
    # Create a mock DataFrame
    df = mock_df()
    # Test with 'Action' genre
    genre = 'Action'
    # Test with 'Long' episode range
    episode_range = 'Long'

    recommendations = get_anime_recommendations(df, genre, episode_range)
    assert len(recommendations) == 1  # Only 'Spy x Family' has 'Long' episode range
    assert recommendations.iloc[0, 0] == 'Spy x Family'

def test_get_anime_recommendations_no_results():
    # Create a mock DataFrame
    df = mock_df()
    # Test with 'Action' genre
    genre = 'Action'
    # Test with 'Long' episode range
    episode_range = 'Short'

    # Call the function with the mock data, genre and episode_range that has no recommendations
    recommendations = get_anime_recommendations(df, genre, episode_range)

    # Assert that the recommendations is None (or handle empty case accordingly)
    assert recommendations is None


# ******************************************************************************************************************************************************
#                                                       TEST CASE 4: anime_recommendation_table
# ******************************************************************************************************************************************************

# Test case for anime_recommendation_table function
def test_anime_recommendation_table():
    # Create a sample DataFrame representing anime recommendations
    recommendations = pd.DataFrame({'title': ['Naruto', 'Spy x Family']})

    # Call the anime_recommendation_table function with the recommendations DataFrame
    table = anime_recommendation_table(recommendations)

     # Assert that the result is of type string (the output should be a formatted table in string form)
    assert isinstance(table, str)

    # Assert that the table contains the name 'Naruto' (this checks if the anime is in the table)
    assert 'Naruto' in table

     # Assert that the table contains the name 'Spy x Family' (this checks if the anime is in the table)
    assert 'Spy x Family' in table


# ******************************************************************************************************************************************************
#                                                       TEST CASE 5: anime_description
# ******************************************************************************************************************************************************

# Test anime_description function
def test_anime_description_valid_choice():
    # Create a mock DataFrame
    df = mock_df()

    # Create mock recommendations DataFrame (simulating the user's recommendations list)
    recommendations = pd.DataFrame({'title': ['Naruto', 'Spy x Family']})

    # Simulate selecting '1' for 'Naruto'
    with patch('builtins.input', return_value='1'):
        result = anime_description(df, recommendations)

    # Define the expected output string correctly
    expected_output = "\n[bold italic light_steel_blue][underline]Anime:[/underline] [/bold italic light_steel_blue][italic light_steel_blue]Naruto[/italic light_steel_blue]\n\n[bold indian_red][underline]Disclaimer:[/underline] \n[/bold indian_red][italic indian_red]Naruto disclaimer[/italic indian_red]\n[bold light_steel_blue]\n[underline]Synopsis:[/underline] \n[/bold light_steel_blue][italic light_steel_blue]Naruto description[/italic light_steel_blue]"
    # Assert that the result matches the expected output
    assert result == expected_output

    #-----------------------------------------------------------------------------------------
    # Simulate selecting '2' for 'Spy x Family'
    with patch('builtins.input', return_value='2'):
        result = anime_description(df, recommendations)

    # Define the expected output string correctly
    expected_output = "\n[bold italic light_steel_blue][underline]Anime:[/underline] [/bold italic light_steel_blue][italic light_steel_blue]Spy x Family[/italic light_steel_blue]\n\n[bold indian_red][underline]Disclaimer:[/underline] \n[/bold indian_red][italic indian_red]Spy x Family disclaimer[/italic indian_red]\n[bold light_steel_blue]\n[underline]Synopsis:[/underline] \n[/bold light_steel_blue][italic light_steel_blue]Spy x Family description[/italic light_steel_blue]"
    # Assert that the result matches the expected output
    assert result == expected_output

# Test case for when the user inputs an invalid choice and then a valid one
def test_anime_description_invalid_choice():
    # Create a mock DataFrame
    df = mock_df()

    # Create mock recommendations DataFrame (simulating the user's recommendations list)
    recommendations = pd.DataFrame({'title': ['Naruto', 'Spy x Family']})

    # Simulate invalid input ('3') followed by a valid input ('2')
    with patch('builtins.input', side_effect=['3', '2']):  # Mock the input to simulate invalid input first, then valid input
        result = anime_description(df, recommendations)  # Call the function to get the description

    # Expected output format with error for invalid input and correct description for 'Spy x Family'
    expected_output = "\n[bold italic light_steel_blue][underline]Anime:[/underline] [/bold italic light_steel_blue][italic light_steel_blue]Spy x Family[/italic light_steel_blue]\n\n[bold indian_red][underline]Disclaimer:[/underline] \n[/bold indian_red][italic indian_red]Spy x Family disclaimer[/italic indian_red]\n[bold light_steel_blue]\n[underline]Synopsis:[/underline] \n[/bold light_steel_blue][italic light_steel_blue]Spy x Family description[/italic light_steel_blue]"

    # Assert if the function's output matches the expected output
    assert result == expected_output

    #-----------------------------------------------------------------------------------------------
    # Simulate empty input ('') followed by a valid input ('1')
    with patch('builtins.input', side_effect=['', '1']):  # Mock the input to simulate invalid input first, then valid input
        result = anime_description(df, recommendations)  # Call the function to get the description

    # Expected output format with error for invalid input and correct description for 'Spy x Family'
    expected_output = "\n[bold italic light_steel_blue][underline]Anime:[/underline] [/bold italic light_steel_blue][italic light_steel_blue]Naruto[/italic light_steel_blue]\n\n[bold indian_red][underline]Disclaimer:[/underline] \n[/bold indian_red][italic indian_red]Naruto disclaimer[/italic indian_red]\n[bold light_steel_blue]\n[underline]Synopsis:[/underline] \n[/bold light_steel_blue][italic light_steel_blue]Naruto description[/italic light_steel_blue]"
    # Assert if the function's output matches the expected output
    assert result == expected_output
