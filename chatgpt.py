#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    print("Error: Please install google-generativeai library")
    print("Run: pip install google-generativeai python-dotenv")
    sys.exit(1)

# Configure Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables")
    print("Please create a .env file with your API key")
    sys.exit(1)

genai.configure(api_key=api_key)

def get_ai_response(prompt):
    """Get response from Gemini API"""
    try:
        # Use Gemini 1.5 Flash (without the 'models/' prefix)
        model = genai.GenerativeModel('gemini-2.5-pro') 
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("AI CLI Interface (Powered by Gemini 2.5 pro)")
    print("Type 'quit' or 'exit' to end the conversation\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        print("AI: ", end="", flush=True)
        response = get_ai_response(user_input)
        print(response + "\n")

if __name__ == "__main__":
    main()