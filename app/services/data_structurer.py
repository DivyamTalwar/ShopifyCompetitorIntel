from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings
from typing import List

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=settings.GEMINI_API_KEY)

def get_structured_faqs(markdown_content: str) -> list:
    if not markdown_content:
        return []
    prompt = f"Extract the Frequently Asked Questions and their answers from the following markdown content:\n\n{markdown_content}"
    response = llm.invoke(prompt)
    return [line for line in response.content.split('\n') if line.startswith("Q:") or line.startswith("A:")]

def extract_contact_info(markdown_content: str) -> dict:
    if not markdown_content:
        return {}
    prompt = f"Extract contact information (emails, phone numbers) from the following markdown content:\n\n{markdown_content}"
    response = llm.invoke(prompt)
    return {"details": response.content}

def extract_social_links(markdown_content: str) -> dict:
    if not markdown_content:
        return {}
    prompt = f"Extract all social media links (Instagram, Facebook, Twitter, etc.) from the following markdown content:\n\n{markdown_content}"
    response = llm.invoke(prompt)
    return {"links": response.content.split()}

def summarize_about_us(markdown_content: str) -> str:
    if not markdown_content:
        return ""
    prompt = f"Summarize the 'About Us' section from the following markdown content:\n\n{markdown_content}"
    response = llm.invoke(prompt)
    return response.content
