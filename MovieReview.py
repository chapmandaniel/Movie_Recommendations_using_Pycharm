import pandas as pd

class MovieReview:
    def __init__(self, user_id, movie_id, movie_title, rating):
        self._user_id = user_id
        self._movie_id = movie_id
        self._movie_title = movie_title
        self._rating = rating
        self._timestamp = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")

    # return the formatted review
    def get_review(self):
        return f"{self._user_id},{self._movie_id},{self._rating},{self._timestamp}\n"

    # Getters
    def get_user_id(self):
        return self._user_id

    def get_movie_id(self):
        return self._movie_id

    def get_movie_title(self):
        return self._movie_title

    def get_rating(self):
        return self._rating

    # Setters
    def set_user_id(self, user_id):
        self._user_id = user_id

    def set_movie_id(self, movie_id):
        self._movie_id = movie_id

    def set_movie_title(self, movie_title):
        self._movie_title = movie_title

    def set_rating(self, rating):
        self._rating = rating
