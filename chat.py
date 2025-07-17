# This is context aware chat
from persistence.memory import workflow_app

config = {"configurable": {"thread_id": "abc123"}}

result = workflow_app.invoke(
    {"input": "What is Dr.Visa's research"},
    config=config,
)

result = workflow_app.invoke(
    {"input": "What is her favorite part of her job?"},
    config=config,
)

print(result["answer"])


