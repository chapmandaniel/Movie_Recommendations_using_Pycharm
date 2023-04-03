import MovieRecommender
import Utils as utils
import MovieReview as MR
import pandas as pd
import os


movieReviews = []


# Get the absolute path of the directory containing your script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the dataset folder dynamically
dataset_folder = os.path.join(script_dir, 'dataset')

# Construct the absolute paths to the ratings.csv and movies.csv files
ratings_csv_path = os.path.join(dataset_folder, 'ratings.csv')
movies_csv_path = os.path.join(dataset_folder, 'movies.csv')

# Read the CSV file
movie_titles = pd.read_csv(movies_csv_path)
# Read the CSV file
movie_ratings = pd.read_csv(ratings_csv_path)

movie_data = pd.merge(movie_ratings, movie_titles, on='movieId')


user_id = 0

while True:
    if user_id == 0:
        utils.welcome_message()
        user_id = utils.get_user_id()
    utils.main_menu()
    choice = input("Enter your choice: ")
    if choice == '1':
        while True:
            # get a random movie from the movie_data dataframe, and get the title
            random_movie = movie_data.sample()
            movie_id = random_movie.iloc[0]["movieId"]
            movie_title = random_movie.iloc[0]["title"]
            # print the name of the movie
            print("\n" + movie_title)
            rating = utils.get_rating()

            if rating == 'q':
                utils.write_reviews(movieReviews, './dataset/ratings.csv')
                print("Thanks for your reviews!")
                break
            elif rating == 's':
                continue
            movieReview = MR.MovieReview(user_id, movie_id, movie_title, rating)
            movieReviews.append(movieReview)
    elif choice == '2':
        print("Analyzing the data... please wait...")
        user_genre = utils.get_user_genre()
        MovieRecommender.get_recommendations(user_id, user_genre)
        movieReviews.clear()
    elif choice == '3':
        user_id = 0
        continue
    elif choice == '4':
        break
    else:
        print("Invalid choice")





