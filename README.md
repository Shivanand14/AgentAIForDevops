Kubernetes AI Agent Code Explanation

This code creates a simple AI-based Kubernetes and Docker assistant using Python, LangChain, and Ollama.

The assistant accepts user questions in normal English, understands the request using an LLM (Large Language Model), executes Kubernetes or Docker commands, and returns the result.

Example:

User asks:

Show me all Kubernetes pods

The assistant automatically runs:

kubectl get pods -A

and displays the output.

Complete Flow

The application works in the following sequence:

User Question
    ↓
AI Agent receives request
    ↓
LLM understands the intent
    ↓
Agent selects appropriate tool
    ↓
Python executes system command
    ↓
Command output returned to LLM
    ↓
Final response displayed to user
Step 1: Importing Required Libraries
import subprocess
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent

These libraries are used to build the AI agent.

subprocess
import subprocess

The subprocess module allows Python to execute operating system commands.

Example:

subprocess.run(["docker","ps"])

This is equivalent to manually typing:

docker ps

in the terminal.

This module is used here to run Kubernetes and Docker commands directly from Python.

ChatOllama
from langchain_ollama import ChatOllama

This connects Python with a locally running LLM through Ollama.

Ollama allows AI models to run locally instead of using cloud services.

In this project, the AI model used is:

qwen3:8b
tool
from langchain_core.tools import tool

The @tool decorator converts a normal Python function into an AI-accessible tool.

Without this decorator, the AI agent cannot use the function.

With @tool, the agent understands:

what the function does
when to use it
how to call it
create_agent
from langchain.agents import create_agent

This is used to create the AI agent.

The agent acts as the coordinator between:

the user
the LLM
and the available tools

It decides which tool should be executed based on the user question.

Step 2: Creating the LLM
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
)

This section initializes the Large Language Model.

model="qwen3:8b"

This specifies which AI model should be used.

qwen3:8b is the selected LLM.

The model is responsible for:

understanding user questions
deciding which tool to use
generating the final response
temperature=0

Temperature controls the randomness of the AI output.

Temperature	Behavior
0	Accurate and consistent
Higher values	More creative/random

For infrastructure and DevOps use cases, accuracy is preferred, so 0 is a good choice.

Step 3: Creating Kubernetes Tool
@tool
def get_pods():

This function creates a Kubernetes-related tool for the AI agent.

The @tool decorator makes the function available to the agent.

Function Description
"""
Lists the pods of a running kubernetes cluster
"""

This description is important because the LLM reads it to understand the purpose of the tool.

The agent uses this information while deciding which tool should handle the user request.

Executing Kubernetes Command
result = subprocess.run(
    ["kubectl", "get", "pods" ,"-A"],
    capture_output=True,
    text=True
)

This executes the following Kubernetes command:

kubectl get pods -A
Meaning of the Command
Part	Meaning
kubectl	Kubernetes CLI
get pods	Retrieve pod details
-A	Show pods from all namespaces

Example output:

NAMESPACE     NAME
default       nginx-pod
kube-system   coredns
capture_output=True

Captures terminal output inside Python.

Without this option, Python cannot store the command result.

text=True

Converts command output into readable text format.

Returning Output
return result.stdout

stdout means standard output.

This returns the command result back to the AI agent.

Step 4: Creating Docker Tool
@tool
def get_docker_containers():

This tool retrieves running Docker containers.

Docker Command
["docker","ps"]

Equivalent terminal command:

docker ps
Purpose

This command lists all active Docker containers.

Example:

CONTAINER ID   IMAGE   STATUS
ab123          nginx   Up 2 hours
Step 5: Creating the AI Agent
agent = create_agent(

This combines:

the LLM
the tools
and the system instructions

into one working AI assistant.

Model Configuration
model=llm

This assigns the previously created LLM to the agent.

Tool Registration
tools=[get_pods,get_docker_containers]

This gives the agent access to:

Kubernetes pod tool
Docker container tool

The agent can now execute these functions whenever required.

System Prompt
system_prompt="You are a helpful agent..."

The system prompt defines the behavior and responsibility of the agent.

It instructs the LLM:

what role it should perform
which tools are available
what type of tasks it should handle

In this case, the agent is configured as a Kubernetes and Docker assistant.

Step 6: Accepting User Input
question = input("Ask your Kubernetes Agent a Question: >")

This line waits for user input.

Example:

Show all running docker containers
Step 7: Executing the Agent
response = agent.invoke(
    {"messages": [("user",question)]}
)

This sends the user question to the AI agent.

The following operations happen internally:

The LLM reads the question
The agent determines which tool is required
The tool executes the system command
Output is returned
The LLM generates the final response
Example Execution Flow

Suppose the user asks:

Show all Kubernetes pods

The internal flow becomes:

User Question
    ↓
LLM understands Kubernetes request
    ↓
Agent selects get_pods()
    ↓
Python runs:
kubectl get pods -A
    ↓
Command output returned
    ↓
Final response shown to user
Step 8: Printing Final Output
print(response["messages"][-1].content)

This prints the final AI-generated response.

response["messages"][-1]
means the latest message returned by the agent.

.content
contains the actual response text.

Key Concepts Used in This Project
Concept	Description
LLM	AI model that understands language
Agent	AI system capable of taking actions
Tool	Function callable by the AI
LangChain	Framework for AI agents
Ollama	Runs local AI models
subprocess	Executes OS commands
Kubernetes	Container orchestration platform
Docker	Container runtime platform
Real-World Use Case

This type of solution is commonly used in:

AIOps platforms
Kubernetes copilots
Infrastructure automation systems
DevOps monitoring assistants
Intelligent support systems

Example capabilities:

checking pod status
retrieving logs
monitoring containers
automating operational tasks
reducing manual troubleshooting
Security Consideration

The assistant can:

understand natural language
execute infrastructure commands
retrieve live system information
and respond intelligently to the user
