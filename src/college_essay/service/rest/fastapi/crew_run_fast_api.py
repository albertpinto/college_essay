from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from college_essay.crew import CollegeEssayCrew

app = FastAPI()

class CrewInput(BaseModel):
    file_content: str
    program: str
    output_file: str
    output_essay: str
    student: str

@app.post("/run-crew")
async def run_crew(input_data: CrewInput):
    try:
        crew = CollegeEssayCrew()
        result = crew.crew().kickoff(inputs=input_data.dict())
        return {"message": "Crew execution successful", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


# def call_run_crew():
#     url = "http://0.0.0.0:8000/run-crew"
#     input_data = {
#         "file_content": "Sample content",
#         "program": "Sample program",
#         "output_file": "output.txt",
#         "output_essay": "essay.txt",
#         "student": "John Doe"
#     }
#     response = requests.post(url, json=input_data)
#     if response.status_code == 200:
#         print("Success:", response.json())
#     else:
#         print("Error:", response.status_code, response.text)

# if __name__ == "__main__":
#     call_run_crew()