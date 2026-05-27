# LLM
import subprocess
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent

# this is coming from Ollama (ollama connect)
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
)

# TOOL
@tool
def get_pods():
    """
    Lists the pods of a running kubernetes cluster
    """
    result = subprocess.run(["kubectl", "get", "pods" ,"-A"],capture_output=True, text=True)
    return result.stdout


@tool
def get_docker_containers():
    """
    Lists the running docker containers
    """
    result = subprocess.run(["docker","ps"],capture_output=True, text=True)
    return result.stdout


# AGENT 
# LLM + TOOLS

agent = create_agent(
    model=llm, 
    tools=[get_pods,get_docker_containers],
    system_prompt="You are a helpful agent that can help in Kubernetes \
        tasks using the tools get_pods \
            you can even help with docker tasks like showing the docker containers using tool \
                get_docker_containers"
    )

question = input("Ask your Kubernetes Agent a Question: >") # user input

response = agent.invoke({"messages": [("user",question)]})

print(response["messages"][-1].content)