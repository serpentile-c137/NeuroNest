import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

# Initialize Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash-8b")

def generate_memory_palace(concepts, session_id):
    prompt = (
    "You are NeuroNest, a memory coach helping someone understand and remember information using the Memory Palace technique.\n\n"
    f"Here is the list of concepts: {', '.join(concepts)}.\n"
    "Create a simple and clear story by placing these concepts in different rooms or scenes of a memory palace.\n"
    "In each room, explain 1–2 concepts using funny, unusual, or exaggerated situations that are easy to imagine.\n"
    "Keep the language simple but do not lose the correct meaning of the concepts.\n"
    "Use bullet points or short paragraphs for each room so it’s easy to follow.\n"
    "The story should be short, clear, and help the person recall the concepts easily.\n"
    "End with a quick summary of all rooms and what each room contained.\n"
    "Only output the final Memory Palace description.\n"
)

    response = model.generate_content(prompt)
    return response.text
