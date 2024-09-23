#!/usr/bin/env python
import sys
from college_essay.crew import CollegeEssayCrew
import json
import re


# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def load_activity_data():
    with open('activity.json', 'r') as file:
        return json.load(file)

def run():
    """
    Run the crew.
    """
    inputs = {
        'program': 'Business',
        'output_file': 'output',
        'activity_file': 'activity',
    }
    
    try:
        CollegeEssayCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"An error occurred during kickoff: {e}")

    try:
        convert_txt_to_json(inputs['activity_file'] + ".txt", inputs['activity_file'] + ".json")
        activity_data = load_activity_data()
        inputs['activity_data'] = activity_data
        for input in inputs:
            print(f"{input}: {inputs[input]}")
    except Exception as e:
        print(f"An error occurred during file conversion: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CollegeEssayCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CollegeEssayCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CollegeEssayCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
    


def parse_activity(lines):
    activity = {}
    current_key = None
    additional_info = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match lines starting with digits followed by a dot (e.g., "1.")
        if re.match(r'^\d+\.', line):
            activity['type'] = line.split('.', 1)[1].strip()

        # Match lines starting with a letter followed by a dot (e.g., "A.")
        elif re.match(r'^[A-Za-z]\.', line):
            current_key = line[0].lower()
            value = line[2:].strip()

            key_mapping = {
                'a': 'position',
                'b': 'organization',
                'c': 'description'
            }
            if current_key in key_mapping:
                activity[key_mapping[current_key]] = value
            else:
                additional_info[current_key] = value

        # Match lines containing a colon (key-value pairs)
        elif ':' in line:
            key, value = map(str.strip, line.split(':', 1))
            key = key.lower().replace(' ', '_')
            value = value.strip()

            if 'grade' in key:
                activity['grade_level'] = value
            elif 'timing' in key:
                activity['timing'] = value
            elif 'hours' in key:
                hours = re.search(r'\d+', value)
                if hours:
                    activity['hours_per_week'] = int(hours.group())
            elif 'weeks' in key:
                weeks = re.search(r'\d+', value)
                if weeks:
                    activity['weeks_per_year'] = int(weeks.group())
            elif 'intend' in key or 'participate' in key:
                activity['continue_in_college'] = value.lower() == 'yes'
            else:
                activity[key] = value

        # Handle additional lines of information
        elif current_key:
            additional_info[current_key] = additional_info.get(current_key, '') + ' ' + line

    # Merge additional info into activity
    for key, value in additional_info.items():
        activity[f'additional_info_{key}'] = value.strip()

    return activity

def parse_awards(lines):
    awards = []
    for line in lines:
        line = line.strip()
        if line.startswith('●'):
            award = {}
            parts = [part.strip() for part in line.strip('● ').split(',')]
            award['name'] = parts[0]

            for part in parts[1:]:
                part_lower = part.lower()
                if 'grade' in part_lower:
                    grade = re.search(r'\d+', part_lower)
                    if grade:
                        award['grade'] = int(grade.group())
                elif any(level in part_lower for level in ['city', 'state', 'national', 'international']):
                    award['level'] = part.capitalize()

            awards.append(award)
    return awards

def convert_txt_to_json(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    # Split content into sections based on blank lines
    sections = re.split(r'\n\s*\n', content)
    activities = []
    awards = []

    for section in sections:
        lines = section.strip().split('\n')
        if not lines:
            continue

        if any('awards' in line.lower() for line in lines):
            awards = parse_awards(lines)
        else:
            activity = parse_activity(lines)
            if activity:
                activities.append(activity)

    data = {
        'activities': activities,
        'awards': awards
    }

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=2)

    print(f"Conversion complete. JSON file saved as {output_file}")