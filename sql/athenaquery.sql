 DROP TABLE job_response_sentiment ;
 CREATE EXTERNAL TABLE IF NOT EXISTS job_response_sentiment (
  Name string,
  Sentiment string,
  SentimentScore struct<Positive : string,
                        Negative : string,
                        Neutral : string,
                        Mixed :string>
   )
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://bucketname/output/' ;

select Name, Sentiment, SentimentScore from  job_response_sentiment ;

SELECT Name, Sentiment, SentimentScore.Positive AS Positive ,  SentimentScore.Negative AS Negative , SentimentScore.Neutral AS Neutral , SentimentScore.Mixed AS Mixed 
FROM  job_response_sentiment
order by Positive desc ;