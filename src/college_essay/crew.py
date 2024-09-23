from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task



# Uncomment the following line to use an example of a custom tool
# from college_essay.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

LLM = 'gpt-4o'

@CrewBase
class CollegeEssayCrew():
	"""CollegeEssay crew"""

	@agent
	def college_question_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['college_question_generator'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			llm=LLM,
			verbose=True
		)
	@task
	def generator_task(self) -> Task:
		"""Generate a college question"""
		return Task(
			config=self.tasks_config['generator_task'],			
			output_file="questions" +".md",
			verbose=True
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CollegeEssay crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
	
	