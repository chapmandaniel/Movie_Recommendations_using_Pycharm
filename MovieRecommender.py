from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.ml.tuning import TrainValidationSplit, ParamGridBuilder
from pyspark.sql.functions import col


def get_recommendations(user_id, genre):
    """
    create the spark session
    load movie ratings
    load movie meta data
    """
    spark = SparkSession.builder \
        .appName("ALS Collaborative Filtering Movie Recommendations") \
        .getOrCreate()

    movieRatings = spark.read.csv("./dataset/ratings.csv", header=True, inferSchema=True)
    movieInfo = spark.read.csv("./dataset/movies.csv", header=True, inferSchema=True)

    # set the log level to ERROR to clean up the console output
    spark.sparkContext.setLogLevel("ERROR")

    # Split the data into train and test sets using the random split function
    (training, test) = movieRatings.randomSplit([0.8, 0.2], seed=42)

    # Build the recommendation model using ALS on the training data initializes an instance of the (ALS)
    # recommendation algorithm from PySpark's MLlib library. ALS is an algorithm used for matrix factorization,
    # a common approach in collaborative filtering for recommendation systems.
    als = ALS(userCol="userId", itemCol="movieId", ratingCol="rating", nonnegative=True, implicitPrefs=False,
              coldStartStrategy="drop")

    param_grid = ParamGridBuilder() \
        .addGrid(als.rank, [10, 50]) \
        .addGrid(als.regParam, [0.01, 0.1]) \
        .build()

    # The evaluator is configured to compute the Root Mean Squared Error (RMSE)
    # between the true ratings and the predicted ratings
    evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")

    tvs = TrainValidationSplit(estimator=als,
                               estimatorParamMaps=param_grid,
                               evaluator=evaluator,
                               trainRatio=0.8)

    model = tvs.fit(training)

    predictions = model.transform(test)
    rmse = evaluator.evaluate(predictions)
    print(f"RMSE: {rmse}")

    # show recommendations for a user
    user_recs = model.bestModel.recommendForAllUsers(1000)
    user_recs = user_recs.filter(user_recs.userId == user_id)

    # First, explode the recommendations array into separate rows
    from pyspark.sql.functions import explode
    exploded_user_recs = user_recs.select("userId", explode("recommendations").alias("recommendation"))

    # Extract movieId and rating from the recommendation struct
    exploded_user_recs = exploded_user_recs.select("userId", "recommendation.movieId", "recommendation.rating")

    # Join the exploded_user_recs DataFrame with the movies DataFrame on movieId
    user_movie_recs = exploded_user_recs.join(movieInfo, on="movieId")

    # limit results to movies that contain the genre selected by the user
    user_movie_recs = user_movie_recs.filter(col('genres').like('%' + genre + '%'))

    user_movie_recs.filter(user_movie_recs.userId == user_id).show(truncate=False)
