import os
from crewai import Agent, LLM
from tools import tool
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.5
)

# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
  role='Blogs Creator from Youtube Videos',
  goal='provide the relevant video suggestions for the topic {topic}',
  verbose=True,
  memory=False,
  backstory=(
    "Expert in understanding videos in AI Data Science, Machine Learning And GEN AI and providing suggestion"
  ),
  tools=[tool],
  llm=llm,
  allow_delegation=True
)

# Creating a writer agent with custom tools and delegation capability
writer = Agent(
  role='Writer',
  goal='Narrate compelling tech stories about the video {topic}',
  verbose=True,
  memory=False,
  backstory=(
    "With a flair for simplifying complex topics, you craft "
    "engaging narratives that captivate and educate, bringing new "
    "discoveries to light in an accessible manner."
  ),
  tools=[tool],
  llm=llm,
  allow_delegation=False
)