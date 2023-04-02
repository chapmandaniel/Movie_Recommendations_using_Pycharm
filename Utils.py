def welcome_message():
    print("\n\nWelcome to the Movie Recommender System")
    print("We will recommend movies based on your reviews!")
    print("=======================================")
    print("\nLets generate a unique ID using your PIN...")


def main_menu():
    print("\n\n=======================================")
    print("1. Submit your review(s)")
    print("2. Get your recommendations")
    print("3. Switch User")
    print("4. Exit")
    print("=======================================")


def get_user_id():
    user_id = input("Enter your PIN: ")
    return user_id


def get_rating():
    while True:
        rating = input("Enter a rating from 0 to 5, q=quit, s=skip: ")
        if rating == 'q':
            return rating
        elif rating == 's':
            return rating
        elif not rating.isnumeric() or float(rating) < 0 or float(rating) > 5:
            print("Invalid rating")
            continue
        else:
            return rating


def write_reviews(movieReviews, csvPath):
    with open(csvPath, 'a') as f:
        for review in movieReviews:
            f.write(review.get_review())


def list_genres():
    return '''
=======================================
Enter a number to select a genre:
    0. All Genres
    1. Action
    2. Adventure
    3. Animation
    4. Comedy
    5. Crime
    6. Documentary
    7. Thriller
    8. Drama
    9. Mystery
=======================================
Enter your choice:
'''

def get_user_genre():
    user_selected_genre = ""
    genre = input(list_genres())
    # if number is not an integer in range 0-9, ask again
    while not genre.isnumeric() or int(genre) < 0 or int(genre) > 9:
        print("\n\nInvalid genre")
        genre = input(list_genres())
    if genre == '0':
        user_selected_genre = ""
    elif genre == '1':
        user_selected_genre = "Action"
    elif genre == '2':
        user_selected_genre = "Adventure"
    elif genre == '3':
        user_selected_genre = "Animation"
    elif genre == '4':
        user_selected_genre = "Comedy"
    elif genre == '5':
        user_selected_genre = "Crime"
    elif genre == '6':
        user_selected_genre = "Documentary"
    elif genre == '7':
        user_selected_genre = "Thriller"
    elif genre == '8':
        user_selected_genre = "Drama"
    elif genre == '9':
        user_selected_genre = "Mystery"
    return user_selected_genre
