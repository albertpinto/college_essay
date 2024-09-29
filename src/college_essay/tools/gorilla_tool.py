from crewai_tools import BaseTool
from langchain_openai import ChatOpenAI

class GorillaSearchTool(BaseTool):
    name: str = "Gorilla based api search tool"
    description: str = (
        "This tool uses the Gorilla LLM to identify the best apis (functions) that are appropriate for a given requirement."
    )

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return self.invoke_gorilla(argument)

    def invoke_gorilla(self, prompt: str, model: str = "gorilla-7b-hf-v1") -> str:
        chat_model = ChatOpenAI(
            openai_api_base="http://zanino.millennium.berkeley.edu:8000/v1",
            openai_api_key="EMPTY",
            model=model,
            verbose=True
            )       
        return chat_model.invoke(prompt).content

# Usage example
if __name__ == "__main__":
    # Create an instance of the tool
    gorilla_tool = GorillaSearchTool()

    # Define the argument (the requirement for which we want to find appropriate APIs)
    argument = "I need an API to convert text to speech"

    # Call the tool
    result = gorilla_tool._run(argument)

    # Print the result
    print(result)