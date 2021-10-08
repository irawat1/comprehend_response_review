import json
import logging
import boto3
import sys
import traceback

#Using logger instead of print.

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')
logger.info('Setting up boto3')

#Using resource instead of client for s3
s3 = boto3.resource('s3')
comprehend = boto3.client('comprehend')

# --------------- Main Lambda Handler ------------------

def lambda_handler(event, context):
    
	# Get the bucket and the sentiment filename triggering the lambda event 
   	
	s3bucket = event['Records'][0]['s3']['bucket']['name']
	s3object = event['Records'][0]['s3']['object']['key']
	logger.info('Reading {} from {}'.format(s3object, s3bucket ))
	
	# Get the sentiment data from the sentiment file for analysis
	
	obj = s3.Object(s3bucket, s3object)
	mailtext = obj.get()['Body'].read().decode("utf-8")
		
	try:
		#Call the comprehend API passing the sentiment text and language. The API returns a JSON object with the sentiment score
		
		sentiment_output = comprehend.detect_sentiment(Text=mailtext, LanguageCode='en')
		logger.info('sentiment_detected')
		
		# As later data will be queried, add the sentiment filename aka company name to the JSON output. Get the name from the triggering object
		
		sentiment_output['Name'] = s3object.partition('.')[0]
		
		# Write the Comprehend API result as filename.sentiment to the output folder of the same input bucket 
		
		s3.Bucket(s3bucket).put_object(Key='output/' + s3object + '.sentiment' , Body=json.dumps(sentiment_output))
        
		return 'Sentiment Successfully Uploaded'
		
	except Exception as e:
		exception_type, exception_value, exception_traceback = sys.exc_info()
		traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
		err_msg = json.dumps({ "errorType": exception_type.__name__, "errorMessage": str(exception_value), "stackTrace": traceback_string})
		logger.error(err_msg)
