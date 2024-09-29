import requests
def call_run_crew( input_data):
    url = "http://localhost:8000/run-crew"
    # input_data = {
    #     "file_content": "Sample content",
    #     "program": "Sample program",
    #     "output_file": "output.txt",
    #     "output_essay": "essay.txt",
    #     "student": "John Doe"
    # }
    response = requests.post(url, json=input_data)
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    if __name__ == "__main__":
        file_path = "/home/albert/Downloads/Rika_Pinto_Resume.txt"
        with open(file_path, "r") as file:
            file_content = file.read()
        
        input_data = {
            "file_content": file_content,
            "program": "Data Science",
            "output_file": "answers",
            "output_essay": "essay",
            "student": "John Doe"
        }
        
        call_run_crew( input_data)