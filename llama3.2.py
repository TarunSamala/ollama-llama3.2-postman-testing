import requests
import socket
import subprocess
import time
import sys

def start_ollama():
    """Start Ollama service and load model"""
    try:
        # Start Ollama server
        server_proc = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server initialization
        time.sleep(8)
        
        # Load model (critical step!)
        model_proc = subprocess.Popen(
            ["ollama", "run", "llama3.2"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for model loading
        time.sleep(12)
        return True
    except FileNotFoundError:
        print("Ollama not installed! Download from https://ollama.ai")
        return False

def is_ollama_alive():
    """Check if port 11434 is open"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', 11434)) == 0

def get_response(prompt):
    if not is_ollama_alive():
        print("Starting Ollama service...")
        if not start_ollama():
            return "Failed to start Ollama"
            
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",  # Use 127.0.0.1 instead of localhost
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=25
        )
        return response.json()["response"]
    except Exception as e:
        return f"Final failure: {str(e)}"

if __name__ == "__main__":
    print("Testing connection...")
    print("Ollama status:", "Live" if is_ollama_alive() else "Dead")
    
    response = get_response("Why was Python failing earlier?")
    print("\nFinal Result:\n", response)