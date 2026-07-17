from groq import Groq

from core.config import settings
# this service is here to talk to our model here groq it is.
# we need to make changes here in order to change the model like openai etc 
# this is abstraction , other services dont need to know how to communicate with llms

class LLMService:   
    # we create a client once only. when app starts , 1 client everyone reuses it. this is fast.
    # if it is inside the func , it will make new client for each request . thats not needed + slow 
    # this _ is convention here . means internal or dont touch outside the class
    _client = Groq(
        api_key=settings.GROQ_API_KEY
    )

    @staticmethod # chat() doesn't depend on any instance-specific state
    # only uses class-level resources like _client, so making it a static method avoids unnecessary object creation.
    def chat(
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float = 0,
    ) -> str:

        response = LLMService._client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt, # these are rules of ai personality
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        content = response.choices[0].message.content.strip() # the response is a huge obj response->choices->message->content
        # we strip extra spaces n newlines

        # llms might return '''json {...}''' we dont want that markdown, we need only json inside so strip these
        if content.startswith("```json"):
            content = content[len("```json"):].strip()

        if content.startswith("```"):
            content = content[len("```"):].strip()

        if content.endswith("```"):
            content = content[:-3].strip()

        return content