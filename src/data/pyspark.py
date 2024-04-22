from __future__ import annotations

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import from_json
from pyspark.sql.functions import to_timestamp
from pyspark.sql.types import DoubleType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructType


class PySparkManagement:
    """Manage PySpark processing"""

    def schema():
        schema = StructType() \
            .add("timestamp", DoubleType()) \
            .add("body", StringType())
        return schema

    def create_spark_session():
        spark = SparkSession.builder \
            .appName("StreamProcessing") \
            .master("spark://spark-master:7077") \
            .getOrCreate()
        return spark

    def create_dataframe(spark):
        df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "reddit_comments") \
            .load()
        return df

    def process_dataframe(df, schema):
        df = df.selectExpr("CAST(value AS STRING)")
        # Parse the JSON string and cast to the right schema
        parsed_df = df.withColumn("data", from_json(col("value"), schema)) \
            .select("data.*")

        # Perform transformations on the parsed data
        # For example, converting the timestamp to a human-readable format
        processed_df = parsed_df.withColumn(
            "timestamp", to_timestamp(col("timestamp")))
        return processed_df

    def view_dataframe(processed_df):
        # Processing and showing the DataFrame (in console for demo purposes)
        # In production, you would write it to a sink, e.g., another Kafka topic, or a database
        query = processed_df.writeStream \
            .outputMode("append") \
            .format("console") \
            .start()
        query.awaitTermination()

    def main(self):
        schema = self.schema()
        spark = self.create_spark_session()
        df = self.create_dataframe(spark)
        processed_df = self.process_dataframe(df, schema)
        self.view_dataframe(processed_df)
        self.stop_spark_session(spark)

    def stop_spark_session(spark):
        spark.stop()
