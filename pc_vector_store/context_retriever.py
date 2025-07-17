from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.prompts import MessagesPlaceholder
from pc_vector_store.retriever import retriever
from llms.chatgpt import llm

### Contextualize question ###
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
### Contextualize LLM ###
contextualize_q_llm = llm.with_config(tags=["contextualize_q_llm"])

history_aware_retriever = create_history_aware_retriever(
    contextualize_q_llm, retriever, contextualize_q_prompt
)