import os
from crewai import Agent, Task, Crew, Process
from langchain_anthropic import ChatAnthropic

os.environ['ANTHROPIC_API_KEY'] = "sk-ant-......"
llm = ChatAnthropic(model="claude-1.3")

from crewai_tools import (
   DOCXSearchTool
)

context = 'New York City, often called simply New York, is the most populous city in the United States. With a 2020 population of 8,804,190 distributed over 300.46 square miles (778.2 km2), New York City is also the most densely populated major city in the United States. Located at the southern tip of the State of New York, the city is the center of the New York metropolitan area, the largest metropolitan area in the world by urban area. With over 20.1 million people in its metropolitan statistical area and 23.5 million in its combined statistical area as of 2020, New York is one of the worlds most populous megacities.'
#we can have the context in a docx file too 
docs_tool = DOCXSearchTool(context)

# Creating Agents
number_retriever_agent = Agent(
    role='Number Retriever',
    goal='Retrieve exact figures and numbers from the given context.',
    backstory='Expert in extracting numbers and figures from text.',
    tools=[docs_tool],
    allow_delegation=False,
    verbose=True,
    llm=llm
)

explanation_retriever_agent = Agent(
    role='Explanation Retriever',
    goal='Retrieve relevant explanations from the given context.',
    backstory='Expert in extracting meaningful explanations from text.',
    tools=[docs_tool],
    allow_delegation=False,
    verbose=True,
    llm=llm
)

boss_agent = Agent(
    role='Boss Agent',
    goal='Combine the retrieved numbers and explanations to provide a comprehensive answer.',
    backstory='Expert in synthesizing information from multiple sources.',
    tools=[],
    allow_delegation=False,
    verbose=True,
    llm=llm
)
# Creating Tasks
number_retriever_task = Task(
    description='Retrieve exact figures and numbers related to the given query.',
    agent=number_retriever_agent,
    tools=[],
    expected_output='Numbers and figures related to the query.',
    extra_content='This task focuses on the most recent developments in AI technology. Prioritize breakthroughs, significant research findings, and major announcements.'
)
explanation_retriever_task = Task(
    description='Retrieve relevant explanations related to the given query.',
    agent=explanation_retriever_agent,
    tools=[],
    expected_output='Explanations related to the query.',
    extra_content='This task focuses on the most recent developments in AI technology. Prioritize breakthroughs, significant research findings, and major announcements.'
)
boss_task = Task(
    description='what is the number of people living in nyc',
    agent=boss_agent,
    context=[number_retriever_task, explanation_retriever_task],
    tools=[],
    expected_output='Comprehensive answer combining numbers and explanations.'
)
# Creating Crew
crew = Crew(
    agents=[number_retriever_agent, explanation_retriever_agent, boss_agent],
    tasks=[number_retriever_task, explanation_retriever_task, boss_task],
    process=Process.hierarchical,
    manager_llm=llm,
    max_rpm=10
)

# Execute the crew

result = crew.kickoff()
print(result)
