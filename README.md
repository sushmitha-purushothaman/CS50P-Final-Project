# CS50P FINAL PROJECT
## Anime Recommendation System

#### Video Demo: https://youtu.be/cE1XfXkitUI?si=UDAA67-YtVzBG62E

#### Description:
Welcome to the **Anime Recommendation System**! This interactive command-line application is designed to help users find the perfect anime based on their preferences. By asking for the user's favorite genre and preferred episode length, the system filters through a dataset of anime and recommends titles that fit those criteria. The system also allows users to view detailed descriptions and disclaimers for each anime, making it an informative and fun tool for anime lovers.

## Overview:
This project is built using Python and leverages the powerful `pandas` library to handle data from an `anime_data.csv` file, which contains information on various anime titles. The `rich` library is used to enhance the user interface by adding color and style to the text, and the `tabulate` library formats the recommendations into an easy-to-read table.

The program works by first asking the user to select their preferred anime genre from a list of available genres, which are extracted from the CSV file. Then, the user selects their preferred episode range from options like "Short," "Medium," "Long," and "Very Long." Based on these selections, the program filters the dataset and returns a list of anime recommendations that match the genre and episode range. The user can choose to see descriptions and disclaimers for each anime, helping them make an informed decision about what to watch next.

The system also includes a feedback mechanism, where users can provide suggestions on how the system can be improved. This feedback is saved to a CSV file for future analysis.

## Files in the Project:
- **anime_data.csv**: This CSV file contains the primary data for the system, including anime titles, genres, episode ranges, descriptions, and disclaimers. This file is the backbone of the recommendation system and must be properly formatted for the system to function correctly.
- **user_feedback.csv**: If the user provides feedback after using the system, this file stores their suggestions for improvement. The file is appended with new feedback after each session, allowing for ongoing updates to the system based on user input.
- **project.py**: This is the main Python script that contains all the logic for the system. It loads the CSV data, presents the user with options, filters the anime based on preferences, and displays recommendations. The script also handles input validation, error handling, and displays results with the help of `rich` and `tabulate`.
- **test_project.py**: This file is an essential addition to this project, providing automated tests to verify the correctness of the application's functions. These tests simulate user input and check whether the filtering logic, recommendation system, and error handling mechanisms are functioning as expected.

  - **get_genre()**: This function displays all available genres and asks the user to select one.
  - **get_episode_range()**: This function asks the user to choose an episode range, filtering out unavailable options based on the selected genre.
  - **get_anime_recommendations()**: Based on the genre and episode range selected, this function filters the dataset and returns anime recommendations.
  - **anime_description()**: If the user wants more details, this function provides the description and disclaimer for a selected anime.
  - **get_user_feedback()**: If the user didn’t enjoy the system, this function allows them to provide feedback, which is stored for future analysis.

## Design Choices:
### User Interaction:
The system uses a command-line interface, which was chosen for simplicity and ease of development. While this could be extended to a GUI in the future, the current design focuses on providing a smooth and intuitive text-based interaction. The choices for genre and episode length are presented in a numbered list, ensuring the user always knows which option they are selecting.

### Data Handling:
The use of `pandas` allows for efficient filtering and processing of the anime dataset, which could potentially grow over time. Data is read from a CSV file, making it easily extensible and manageable. This also means that users can add or modify the anime data without altering the core logic of the system.

### Error Handling:
A variety of exceptions are handled to ensure the system is robust. For instance, if the anime data file is missing or improperly formatted, the system catches those errors and displays a meaningful message to the user. Input validation is also carefully implemented, ensuring that the user selects valid options for genres and episode ranges.

### Feedback System:
The feedback system is an essential part of ensuring that the system improves over time. By saving user feedback to a CSV file, the project remains open to future iterations based on real user experiences. This allows the developer to analyze common suggestions and identify areas of improvement.

## Conclusion:
The Anime Recommendation System is a fun and useful tool for anime enthusiasts, providing personalized recommendations based on genre and episode length. The system is easily extendable and could be improved with additional features like filtering by ratings, adding more detailed user preferences, or even integrating with external databases. The user-friendly design and clear feedback mechanism make it an ideal starting point for a more robust anime discovery platform.
