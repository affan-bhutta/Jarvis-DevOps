# client.py
import requests
import json

def ask_ai_openrouter(question):
    """Call OpenRouter API"""
    AI_API_KEY = "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"
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {AI_API_KEY}",  
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": [
					{
						"role": "system", 
						"content": "You are JARVIS, a helpful AI assistant. You speak clearly and concisely. Keep answers as short as possible."
					},
					{
						"role": "user",
						"content": question
					}
				]
            })
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return f"API Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Connection error: {str(e)}"

# Test the API
if __name__ == "__main__":
    test_response = ask_ai_openrouter("Hello, who are you?")
    print("Test response:", test_response)