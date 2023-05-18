from flask import Flask, request, jsonify, send_file, Response
import json
import logging

from noisytext import generate_text_on_gaussian
from common import get_random_text, red, green, print_divider

app = Flask(__name__)

#logging.getLogger('werkzeug').disabled = True

teams_seen_t1 = {'<INSERT TEAMNAME HERE>'}

@app.route("/t1/retrieve", methods=['POST', 'GET'])
def get_ocr():
    # Get team name / members from POST
    if request.method == 'POST':
        try:
            team_name = request.json['team_name'].strip()

        except KeyError:
            return "Must provide team name / members", 400
        
        except Exception as e:
            return f"Error with input: {e}", 400
        
        text_to_gen = get_random_text(team_name)


    else:
        text_to_gen = get_random_text()
    

    # Generate bytes of noisy text image
    jpg_bio = generate_text_on_gaussian(text_to_gen)

    # Return in request
    return Response(jpg_bio.getvalue(), mimetype='image/jpg')


@app.route("/t1/submit", methods=['POST'])
def submit_ocr():
    # Get payload
    payload = request.json
    team_name = payload['team_name'].strip()
    members = payload['members']
    submission = payload['submission']
    
    # Check if the value is what was expected
    expected = get_random_text(team_name)
    
    if submission.strip() == expected.strip():
        if team_name not in teams_seen_t1:
            print()
            print_divider()
            print(green(f"SUCCESS! Team '{team_name}' successfully performed OCR"))
            display_members = '\n'.join(members)
            print(f"Well done to:\n {display_members}")
            print("We'll come around and make sure you haven't cheated...")
            print_divider()
            teams_seen_t1.add(team_name)

    else:
        print()
        print_divider()
        print(f"{red('INCORRECT:')} Team '{team_name}' {red('incorrectly performed OCR')}")
        print("You provided: " + submission.strip())
        print("We expected: " + expected.strip())
        print(green("Keep trying!"))
        print_divider()

    return "", 200


@app.route("/t3/submit", methods=['POST'])
def submit_drawing():
    # Get payload
    payload = json.loads(request.files['json'].read().decode())
    team_name = payload['team_name'].strip()
    members = payload['members']
    submission_file = request.files['file']
    
    # Save the file in a folder named by teamname
    if not os.path.isdir(f"t3/{team_name}"):
        os.makedirs(f"t3/{team_name}")

    submission_file.save(f"t3/{team_name}/submission_{len(os.listdir('t3/'+team_name))}.jpg")
    return "", 200

if __name__ == '__main__':
    import os
    os.system("clear")
    os.system("cls")
    print_divider()
    print(green("Now accepting submissions"))
    print_divider()
    app.run(host='localhost', port=8085)
