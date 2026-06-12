import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

from crewai import LLM
llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.5
)

from crewai import Agent
from tools import tool

# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
  role='Senior Researcher',
  goal='Uncover groundbreaking technologies in {topic}',
  verbose=True,
  memory=False,
  backstory=(
    "Driven by curiosity, you're at the forefront of "
    "innovation, eager to explore and share knowledge that could change "
    "the world."
  ),
  tools=[tool],  # tools go on the Agent, not the Task
  llm=llm,
  allow_delegation=True
)

# Creating a writer agent with custom tools and delegation capability
writer = Agent(
  role='Writer',
  goal='Narrate compelling tech stories about {topic}',
  verbose=True,
  memory=False,
  backstory=(
    "With a flair for simplifying complex topics, you craft "
    "engaging narratives that captivate and educate, bringing new "
    "discoveries to light in an accessible manner."
  ),
  tools=[tool],  # tools go on the Agent, not the Task
  llm=llm,
  allow_delegation=False
)

from crewai import Task

# Research task — no tools= here
research_task = Task(
  description=(
    "Identify the next big trend in {topic}."
    "Focus on identifying pros and cons and the overall narrative."
    "Your final report should clearly articulate the key points,"
    "its market opportunities, and potential risks."
  ),
  expected_output='A comprehensive 3 paragraphs long report on the latest AI trends.',
  agent=researcher,
)

# Writing task — no tools= here
write_task = Task(
  description=(
    "Compose an insightful article on {topic}."
    "Focus on the latest trends and how it's impacting the industry."
    "This article should be easy to understand, engaging, and positive."
  ),
  expected_output='A 4 paragraph article on {topic} advancements formatted as markdown.',
  agent=writer,
  async_execution=False,
  output_file='new-blog-post.md'
)

from crewai import Crew, Process

# Forming the tech-focused crew
crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, write_task],
  process=Process.sequential,
  memory=False,
  cache=True,
  max_rpm=100
)

# Starting the task execution process
result = crew.kickoff(inputs={'topic': 'AI in healthcare'})
print(result)