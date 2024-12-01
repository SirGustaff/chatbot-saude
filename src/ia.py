from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from src import prompts


api_key='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'

class Ia: 
   
    def responder_pergunta_unica(self, configuracao, pergunta):
        
      chat = ChatGroq(temperature=0, groq_api_key='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', model_name='llama3-8b-8192')

      system = configuracao
      human = "{text}"

      prompt = ChatPromptTemplate.from_messages(
         [
            ("system", system), ("human", human)
          ]
      )

      chain = prompt | chat

      return (chain.invoke({"text": pergunta})).content
    
    def iniciar_chat_constante(self, memoria_tamanho=10):
       
        chat = ChatGroq(temperature=0, groq_api_key=api_key, model_name='llama3-8b-8192')
        
        memory = ConversationBufferWindowMemory(k=memoria_tamanho, memory_key="chat_history", return_messages=True)

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=prompts.chat_prompt),  # Configuração inicial
                MessagesPlaceholder(variable_name="chat_history"),  # Histórico da conversa
                HumanMessagePromptTemplate.from_template("{human_input}")  # Entrada do usuário
            ]
        )

        # Criando a cadeia de interação
        conversation_chain = LLMChain(
            llm=chat,
            prompt=prompt,
            memory=memory,
            verbose=False
        )

        return conversation_chain