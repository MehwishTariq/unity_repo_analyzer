from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool

from unity_repo_reader.helper.report_path_resolver import SmartReportPathResolver
from unity_repo_reader.tools.custom_unity_tool import UnityCSharpMapperTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class UnityRepoReader():
    """UnityRepoReader crew"""

    def __init__(self, project_name: str = "default_project"):
        self.project_name = project_name

    agents: list[BaseAgent]
    tasks: list[Task]

    # YAML config locations (must match files under src/unity_repo_reader/config)
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    # Initialize your pure Python helper
    path_resolver = SmartReportPathResolver()
    
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def crawler(self) -> Agent:
        return Agent(
            config= self.agents_config['crawler'],# type: ignore
            tools=[UnityCSharpMapperTool()],
            verbose=True
        )

    @agent
    def evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config['evaluator'],# type: ignore
            tools=[FileReadTool()],  # The evaluator can read files if needed for deeper analysis
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],# type: ignore
            tools=[],  # The writer operates entirely on text summaries provided as context
            verbose=True
        )

    # --- Tasks Definitions ---
    @task
    def crawler_task(self) -> Task:
        return Task(
            config=self.tasks_config['crawler_task']# type: ignore
        )

    @task
    def evaluator_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluator_task'],# type: ignore
            context=[self.crawler_task()]  ## type: ignore Automatically passes the structural map output to the evaluator
        )

    @task
    def writer_task(self) -> Task:
        
        task_config = self.tasks_config['writer_task'] # type: ignore
     
        # Run standard python logic to get the string
        resolved_output_path = self.path_resolver.resolve_output_path(project_name=self.project_name)
        
        # Lock the string into the CrewAI config dictionary
        task_config['output_file'] = resolved_output_path #type: ignore
        
        return Task(
            config=task_config,
            context=[self.evaluator_task()], #type: ignore Passes the structural evaluation to the writing phase
        )
        
    @crew
    def crew(self) -> Crew:
        """Creates the GithubRepoReader crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
