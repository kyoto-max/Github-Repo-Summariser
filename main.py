from github import Github,GithubException
import base64
from google.colab import userdata
from groq import Groq

# ------------------------------------------------------------------------------------------------

def get_repo_data(repo_path="PyGithub/PyGithub"):
    g = Github()

    ALLOWED_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.c', '.cpp', '.md', '.txt', '.json', '.html', '.css'}
    IGNORED_DIRS = {'node_modules', '.git', 'venv', '__pycache__', 'dist', 'build', 'tests'}
    MAX_FILE_SIZE = 30000

    try:
        repo = g.get_repo(repo_path)
        contents = repo.get_contents("")

        with open("prompt.txt", "w", encoding='utf-8') as file:
            file.write(f"You are a senior technical architect. Below is the source code for a project.\n 1. Summarize the project's core architecture.\n2. Rate it (1-10) based on code quality and documentation.\n3. Suggest 3 specific code improvements.\n")

            while contents:
                file_content = contents.pop(0)

                if file_content.type == "dir":
                    if file_content.name not in IGNORED_DIRS:
                        contents.extend(repo.get_contents(file_content.path))
                    continue


                import os
                _, ext = os.path.splitext(file_content.name)
                if ext.lower() not in ALLOWED_EXTENSIONS:
                    continue


                if file_content.size > MAX_FILE_SIZE:
                    print(f"Skipping {file_content.name} (Too large: {file_content.size} bytes)")
                    continue

                try:
                    decoded_text = base64.b64decode(file_content.content).decode('utf-8')
                    file.write(f"--- FILE: {file_content.path} ---\n")
                    file.write(decoded_text + "\n\n")
                except:
                    continue

        print("Done! Filtered context saved to prompt.txt")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        g.close()
# ------------------------------------------------------------------------------------------------

def call_groq():
    client = Groq(api_key=userdata.get('Groq_Key'))

    with open("prompt.txt", "r") as f:
        repo_context = f.read()

    print("Groq is analyzing your code...")
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": repo_context,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    print(response.choices[0].message.content)

# ------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    get_repo_data()
    call_groq()
