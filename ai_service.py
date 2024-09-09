import anthropic
import logging

class AIService:
    def __init__(self, api_key):
        self.client = anthropic.Client(api_key=api_key)
        self.logger = logging.getLogger(__name__)

    def summarize(self, query, search_results):
        try:
            content = f"Query: {query}\n\nSearch Results:\n"
            for result in search_results[:5]:  # Ограничимся первыми 5 результатами
                content += f"- {result['title']}: {result['content'][:200]}...\n\n"
            
            content += "\nProvide a brief summary of these search results in 2-3 sentences."

            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=150,
                temperature=0,
                system="You are a helpful assistant that provides brief summaries.",
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            self.logger.error(f"Error summarizing with Anthropic API: {str(e)}")
            return None