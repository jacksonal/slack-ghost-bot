import os
import json
import urllib, urllib.request
import random

my_user_id = "U8NJCPQ1F"
delete_responses = [
    "There was something here, it's gone now.",
    "I sense a disturbance in the force...",
    "A glitch in the matrix?",
    "How embarassing!",
    "I hope no one saw that.",
    ";)",
    "It's for the best, really.",
    "Aw shit. Here we go again.",
    "WAIT! WHAT DID YOU SAY!?",
    "Did you make a typo?",
    "Where da text at?!",
    "if you can't say something nice, don't say nothin' at all",
    "THE GHOST KNOWS! THE GHOST ALWAYS WATCHING"
]

def send_text_response(event, response_text):
    SLACK_URL = "https://slack.com/api/chat.postMessage"
    body = event.get("body")
    slack_body = json.loads(body)
    print(f"slack event received:\n {json.dumps(slack_body)}")
    #for debugging. only care about my messages
    channel_id = slack_body.get("event").get("channel")
    
    data = urllib.parse.urlencode(
        (
            ("token", os.environ["BOT_TOKEN"]),
            ("channel", channel_id),
            ("text", response_text)
        )
    )
    data = data.encode("ascii")
    
    request = urllib.request.Request(SLACK_URL, data=data, method="POST")
    request.add_header( "Content-Type", "application/x-www-form-urlencoded" )
    
    # Fire off the request!
    print("Messaging Slack...")
    x = urllib.request.urlopen(request).read()
def lambda_handler(event, context):
    print(f"Received event:\n{json.dumps(event)}\nWith context:\n{context}")
    slack_body = event.get("body")
    slack_event = json.loads(slack_body)
    if "challenge" in slack_event:
        challenge_answer = slack_event.get("challenge")
        
        return {
            'statusCode': 200,
            'body': challenge_answer
        }
    else:
        if slack_event.get("event").get("type") == 'message':
            if slack_event.get("event").get("subtype") == 'message_deleted' and 'previous_message' in slack_event.get("event"):
                send_text_response(event, random.choice(delete_responses))
        
        return {
            'statusCode': 200
        }