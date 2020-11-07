from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
#import os
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 pyspark-shell'

def main():
    """
    Função principal.
            Retorno: None
    """
    spark = SparkSession.builder.appName("kafka_consumer").getOrCreate()
    '''
    schema = StructType() \
        .add("userid", IntegerType()) \
        .add("pageid", IntegerType())
    '''    
    df = spark \
         .readStream \
         .format("kafka") \
         .option("kafka.bootstrap.servers", "kafka_confluent:9094") \
         .option("subscribe", "pageviews") \
         .load() \
         .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
         #.select(from_json(col("value").cast("string"), schema).alias("parsed"))

    df_sink = df \
         .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
         .writeStream \
         .format("kafka") \
         .option("kafka.bootstrap.servers", "kafka_confluent:9094") \
         .option("topic", "pageviews-mirror") \
         .option("checkpointLocation", "./checkpointLocation") \
         .start()
    df_sink.awaitTermination();     

if __name__ == "__main__":
        main()