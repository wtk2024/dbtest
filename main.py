from flask import Flask, request, jsonify
import json
import os
from github import Github  # PyGithub library

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()  # Get JSON data from the request
    
    # Path to the JSON file
    json_file_path = 'data.json'

    # Load existing data
    existing_data = []
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            existing_data = json.load(file)

    # Append new data
    existing_data.append(data)

    # Write updated data to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

    # Commit and push changes to GitHub
    commit_to_github(json_file_path)

    return jsonify({'message': 'Data saved successfully!'})

def commit_to_github(file_path):
    # Authenticate with GitHub
    g = Github("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")  # Replace with your GitHub access token
    repo = g.get_user().get_repo("Ydbtest")  # Replace with your repository name
    with open(file_path, "rb") as file:
        repo.update_file(file_path, "Updated data.json", file.read(), repo.get_contents(file_path).sha)

if __name__ == '__main__':
    app.run(debug=True)
