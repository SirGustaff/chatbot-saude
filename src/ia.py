from groq import Groq


api_client = Groq(
  api_key='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'
)

class Ia: 
   
    def responder_pergunta_unica(self, configuracao, pergunta):
        chat_completion = api_client.chat.completions.create(
            messages=[
                {
                  "role": "system",
                  "content": configuracao
                },
                {
                    "role": "user",
                    "content": pergunta, 
                }
            ],
            model="llama3-8b-8192",
        )

        return(chat_completion.choices[0].message.content)
    