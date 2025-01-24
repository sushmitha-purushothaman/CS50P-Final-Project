import os
import pandas as pd
from rich import print
from tabulate import tabulate


# Main function to run the anime recommendation system
def main():
    try:
        # Read the anime data from a CSV file
        anime_df = pd.read_csv(r'anime_data.csv', encoding ='ISO-8859-1')

        # Check for missing or essential columns after reading the file
        required_columns = ['title', 'genre', 'episode_range', 'description', 'disclaimer']
        missing_columns = [col for col in required_columns if col not in anime_df.columns]

        if missing_columns:
            print(f"[bold indian_red]Error: Missing required columns: {', '.join(missing_columns)}[/bold indian_red]")
            return

    except FileNotFoundError:
        print("[bold indian_red]Error: The specified file was not found.[/bold indian_red]")
        return
    except pd.errors.EmptyDataError:
        print("[bold indian_red]Error: The file is empty.[/bold indian_red]")
        return
    except pd.errors.ParserError:
        print("[bold indian_red]Error: There was an issue parsing the file.[/bold indian_red]")
        return
    except UnicodeDecodeError:
        print("[bold indian_red]Error: The file encoding is invalid. Please check the file encoding.[/bold indian_red]")
        return
    except Exception as e:
        print(f"[bold indian_red]An error occurred while loading the file: {str(e)}[/bold indian_red]")
        return

    # Terminal size and separator for display formatting
    terminal_width = os.get_terminal_size().columns
    dashed_line = '-' * terminal_width

    # Display system greeting
    print(f"[bold purple]{dashed_line}[/bold purple]")
    title = "Hi!👋  Welcome to Anime Recommendation System!😊"
    print(f"[bold slate_blue1]{title}[/bold slate_blue1]")
    print(f"[bold purple]{dashed_line}[/bold purple]")

    # Main loop for the anime recommendation process
    while True:
        menu = "[bold slate_blue1]MAIN MENU: [/bold slate_blue1]"
        print(f"\n{menu}")

        print("\n[bold italic light_steel_blue]Please select your preferences so we can recommend the perfect anime for you![/bold italic light_steel_blue]\n")

        # Get genre and episode range preferences from the user
        genre = get_genre(anime_df)
        print(f"[bold italic light_steel_blue]\nAwesome! Since you prefer [gold1]{genre}[/gold1] let's narrow down your preferences by choosing the story length. Once we have that, we can give you some tailored anime recommendations![/bold italic light_steel_blue]")

        episode_range = get_episode_range(anime_df, genre)

        # Get anime recommendations based on the selected preferences
        recommendations = get_anime_recommendations(anime_df, genre, episode_range)

        if recommendations is not None:
            print(f"[bold italic light_steel_blue]\nThanks for your answers! Based on your preferences, here are the anime series we recommend:[/bold italic light_steel_blue]\n")
            print(anime_recommendation_table(recommendations))

            # Ask if the user wants to see a description of the recommended anime
            if len(recommendations) > 1:
                description = get_choice("\n[bold green1]Would you like to get a description for any of the above recommended anime? (Enter 'Y' for Yes/'N' for No): [/bold green1]")
            else:
                description = get_choice("\n[bold green1]Would you like to get a description for the above recommended anime? (Enter 'Y' for Yes/'N' for No): [bold green1]")

            if description:
                print(anime_description(anime_df, recommendations))
                if len(recommendations) > 1:
                    while True:
                        question = "\n[bold green1]Would you like to continue seeing the description for any other anime from above? (Enter 'Y' for Yes/'N' for No): [/bold green1]"
                        description = get_choice(question)
                        if description:
                            print(anime_description(anime_df, recommendations))
                        else:
                            break
        else:
            print("[bold dark_orange]Sorry! No anime is currently available in our system for the given genre and episode range 😟[/bold dark_orange]")

        # Ask if the user wants to go back to the main menu or exit
        return_main_menu_question = "\n[bold green1]Would you like to go back to the main menu to explore more options? (Enter 'Y' to go back to Main menu/Enter 'N' to exit the system): [/bold green1]"
        choice = get_choice(return_main_menu_question)  # Get user input
        if choice:
            print(f"[bold purple]\n{dashed_line}[/bold purple]")
            continue
        else:
            print()
            print(f"[bold purple]{dashed_line}[/bold purple]")
            exit_message = "\t\t\tYou have successfully exited the main menu!"
            for word in exit_message:
                print(f"[yellow1]{word} [/yellow1]", end="")
            break

    print(f"[bold purple]\n{dashed_line}[/bold purple]")

    print("[italic bold underline orange1]\nTell us what you think?[italic bold underline orange1]")
    # Ask for user feedback if they did not enjoy the system
    user_satisfaction_question = "\n[bold orange1]Did you enjoy the Anime Recommendation System? (Enter 'Y' for Yes/'N' for No): [bold orange1]"
    liked_system = get_choice(user_satisfaction_question)
    if liked_system:
        print("[italic bold orange1]\nWe're so glad you enjoyed it![/italic bold orange1]😊[italic bold orange1] (Feel free to try again anytime!)[/italic bold orange1]")
    else:
        user_suggestion = get_user_feedback()
        try:
            # Save user feedback to CSV
            if not os.path.exists('user_feedback.csv'):
                user_suggestion.to_csv('user_feedback.csv', mode='w', header=True, index=False)
            else:
                user_suggestion.to_csv('user_feedback.csv', mode='a', header=False, index=False)
            print("[italic bold orange1]\nThank you for your valuable feedback![/italic bold orange1]")
        except Exception as e:
            print(f"[bold indian_red]Error saving feedback: {str(e)}[/bold indian_red]")

    # Closing message
    thank_you_message = "Thanks you for exploring our anime recommendation system! Happy watching!😄"
    print()
    print(f"[bold purple]{dashed_line}[/bold purple]")
    print(f"[bold slate_blue1]{thank_you_message}[/bold slate_blue1]")
    print(f"[bold purple]{dashed_line}[/bold purple]\n")


# Function to get the user's preferred anime genre
def get_genre(df):
         # Split genres by commas, remove duplicates, and get unique genres
        all_genres = df['genre'].str.split(', ').explode()
        unique_genres = all_genres.unique()

        # Display available genres for the user
        print("[bold slate_blue1]1. Genre Preferences[/bold slate_blue1]")
        print("[italic slate_blue1]\n\tWhat kind of anime are you in the mood for today?[/italic slate_blue1]")

        # List the genres for the user to choose from
        for i, genre in enumerate(unique_genres, start=1):
            print(f"[italic slate_blue1]\t{i}. {genre}[/italic slate_blue1]")

        # Loop until the user selects a valid genre
        while True:
            print("\n[bold green1]\tEnter a number corresponding to your preferred genre: [/bold green1]", end="")
            try:
                genre_choice = int(input())  # Get the user's choice as input
                if 1 <= genre_choice <= len(unique_genres):
                    return unique_genres[genre_choice - 1]  # Return selected genre
                else:
                    print("[bold indian_red]\tInvalid choice. Please select a number from the list.[/bold indian_red]")
            except ValueError:
                print("[bold indian_red]\tInvalid choice. Please select a number from the list.[/bold indian_red]")


# Function to get the preferred episode range for the chosen genre
def get_episode_range(df, genre):
    # Filter dataframe for the chosen genre
    filtered_df = df[df['genre'].str.contains(genre, case=False, na=False)]  # case insensitive search

    # Get unique episode ranges for the selected genre
    filtered_genre_episode_range = filtered_df['episode_range'].unique()
    unique_episode_range_list = df['episode_range'].unique()

    # Define available episode ranges and their descriptions
    episode_range_flags = {
        "Short": "1 to 15 episodes",
        "Medium": "16 to 30 episodes",
        "Long": "31 to 100 episodes",
        "Very Long": "101+ episodes"
    }

    available_ranges = {}  # Dictionary to track which episode ranges are available for the chosen genre

    # Display the available episode ranges for the genre
    print("[bold slate_blue1]\n2. Story Length[/bold slate_blue1]")
    print("[italic slate_blue1]\n\tHow long do you prefer the anime to be?[/italic slate_blue1]")

    # List the episode ranges with availability for the chosen genre
    for i, (label, range_desc) in enumerate(episode_range_flags.items(), 1):
        if label in filtered_genre_episode_range:
            print(f"[italic slate_blue1]\t{i}. {label} ({range_desc})[/italic slate_blue1][sea_green3] \t-- Available[/sea_green3]")
            available_ranges[i] = label
        else:
            print(f"[italic slate_blue1]\t{i}. {label} ({range_desc})[/italic slate_blue1][indian_red] \t-- Not available[/indian_red]")

    # Loop until the user selects a valid episode range
    while True:
        try:
            print("\n\t[bold green1]Enter a number corresponding to your preferred episode range: [/bold green1]", end="")
            episode_choice = int(input())

            if 1 <= episode_choice <= len(unique_episode_range_list):
                if episode_choice in available_ranges:
                    return available_ranges[episode_choice]  # Return the selected episode range
                else:
                    print("[bold indian_red]\tPlease choose an episode range that is currently available.[/bold indian_red]")
            else:
                print("[bold indian_red]\tError: Invalid input. Please enter a valid number from the list.[/bold indian_red]")
        except:
            print("[bold indian_red]\tError: Invalid input. Please enter a valid number from the list.[/bold indian_red]")


# Function to filter and get anime recommendations based on genre and episode range
def get_anime_recommendations(df, genre, episode_range):
    # Filter dataframe for the selected genre
    filtered_df = df[df['genre'].str.contains(genre, case=False, na=False)]

    # Filter by episode range
    if episode_range == "Short":
        filtered_df = filtered_df[filtered_df['episode_range'] == "Short"]
    elif episode_range == "Medium":
        filtered_df = filtered_df[filtered_df['episode_range'] == "Medium"]
    elif episode_range == "Long":
        filtered_df = filtered_df[filtered_df['episode_range'] == "Long"]
    elif episode_range == "Very Long":
        filtered_df = filtered_df[filtered_df['episode_range'] == "Very Long"]

    # If recommendations are found, return the titles
    if not filtered_df.empty:
        recommendations = filtered_df[['title']]
        return recommendations
    else:
        return None  # Return None if no recommendations found


# Function to format the anime recommendations into a table for display
def anime_recommendation_table(recommendations):
    if recommendations is not None and not recommendations.empty:
        table_headers = ["No.", "Anime"]

        # Prepare table data
        table_data = [(i, anime) for i, anime in enumerate(recommendations['title'], start=1)]

        # Return a formatted table of recommendations
        return tabulate(table_data, headers=table_headers, tablefmt="fancy_grid", numalign="left", stralign="left")
    else:
        return "[bold indian_red]No anime recommendations found for your preferences![/bold indian_red]"


# Function to show the anime description based on user's choice
def anime_description(df, recommendations):
    while True:
        try:
            if len(recommendations) > 1:
                print("[bold green1]\nPlease enter the number corresponding to the anime you want a description for: [/bold green1]", end="")
                choice = input().strip()  # Get user input
            else:
                choice = 1  # Automatically select the only anime if there is just one

            choice = int(choice) - 1  # Convert to zero-indexed

            if choice < 0 or choice >= len(recommendations):
                print("[bold indian_red]Error: Invalid choice! Please enter a valid number from the list.[/bold indian_red]")
            else:
                anime = recommendations.iloc[choice]['title']
                anime_row = df[df['title'] == anime].iloc[0]

                # Display the anime's disclaimer and description
                anime_disclaimer = anime_row['disclaimer']
                anime_description = anime_row['description']

                # Provide default text if the disclaimer or description is empty
                if pd.isna(anime_disclaimer) or anime_disclaimer.strip() == "":
                    anime_disclaimer = "[italic light_steel_blue]No specific disclaimer available.[/italic light_steel_blue]"

                if pd.isna(anime_description) or anime_description.strip() == "":
                    anime_description = "[italic light_steel_blue]No detailed description available.[/italic light_steel_blue]"

                # Return the formatted description
                return f"\n[bold italic light_steel_blue][underline]Anime:[/underline] [/bold italic light_steel_blue][italic light_steel_blue]{anime}[/italic light_steel_blue]\n\n[bold indian_red][underline]Disclaimer:[/underline] \n[/bold indian_red][italic indian_red]{anime_disclaimer}[/italic indian_red]\n[bold light_steel_blue]\n[underline]Synopsis:[/underline] \n[/bold light_steel_blue][italic light_steel_blue]{anime_description}[/italic light_steel_blue]"

        except ValueError:
            print("[bold indian_red]Error: Invalid input! Please enter a valid number from the list.[/bold indian_red]")


# Function to get user's choice (yes or no) for certain actions
def get_choice(question):
    while True:
        try:
            print(f"{question}", end="")

            choice = input().strip().lower()  # Get user input

            if choice == 'y':
                return True  # Yes choice
            elif choice == 'n':
                return False  # No choice
            else:
                print("[bold italic indian_red]Error: Invalid input, please answer with 'Y' or 'N'.[/bold italic indian_red]")
                continue

        except Exception as e:
            print("[bold italic indian_red]Error: Invalid input, please answer with 'Y' or 'N'.[/bold italic indian_red]")
# Function to collect user feedback if they did not like the system
def get_user_feedback():
    print("[bold italic orange1]\nWe're sorry to hear that![/bold italic orange1]😔[bold italic orange1] Could you please let us know how we can improve.[/bold italic orange1]")
    print("[bold orange1]\nYour thoughts: [/bold orange1]", end= "")
    improvement_suggestion = input()

    # Save the suggestion in a DataFrame for later use
    feedback_data = pd.DataFrame({
        'Timestamp': [pd.Timestamp.now()],
        'Suggestion': [improvement_suggestion]
    })

    return feedback_data


# Entry point for the program
if __name__ == "__main__":
    main()
