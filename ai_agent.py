import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

# Initialize Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash-8b")

def generate_memory_palace(concepts, session_id):
    """Generate a memory palace story using Google's Gemini AI"""
    prompt = (
    "You are NeuroNest, a memory coach helping someone understand and remember information using the Memory Palace technique.\n\n"
    f"Here is the list of concepts: {', '.join(concepts)}.\n"
    "Create a simple and clear story that connects these concepts in a creative and memorable way.\n"
    "Explain 1–2 concepts at a time using funny, unusual, or exaggerated situations that are easy to imagine.\n"
    "Keep the language simple but do not lose the correct meaning of the concepts.\n"
    "Use bullet points or short paragraphs so it’s easy to follow.\n"
    "The story should be short, clear, crisp and help the person recall the concepts easily.\n"
    "End with a quick summary of the full story and how the concepts were linked.\n"
    "Only output the final memory story.\n"
)


    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating memory palace: {e}")
        return f"Sorry, I couldn't generate a memory palace right now. Please try again later.\n\nError: {str(e)}"

def generate_quiz_questions(concepts, story):
    """Generate quiz questions based on the memory palace story"""
    prompt = (
        f"Based on this memory palace story:\n{story}\n\n"
        f"And these concepts: {', '.join(concepts)}\n\n"
        "Create 3-5 multiple choice questions to test understanding of the concepts.\n"
        "Each question should have 4 options (A, B, C, D) (make sure options are printed on new line) with only one correct answer.\n"
        "Make the questions engaging and related to the memory palace story.\n"
        "Format as:\n"
        "**Question 1:** [question text]\n"
        "A) [option]\n\n"
        "B) [option]\n\n" 
        "C) [option]\n\n"
        "D) [option]\n\n"
        "**Correct Answer:** [letter]\n\n\n"
    )
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return "Sorry, I couldn't generate quiz questions right now."