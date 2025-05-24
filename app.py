import os
from flask import Flask, render_template, request, send_file
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

app = Flask(__name__)

# Load API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set")

# Load and prepare prompt template
prompt = PromptTemplate(
    input_variables=["resume"],
    template=open("prompt.txt").read()
)

# Initialize LLM and chain
llm = ChatOpenAI(model="gpt-4", temperature=0.7, openai_api_key=openai_api_key)
chain = LLMChain(llm=llm, prompt=prompt)

# Flask route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume = request.form["resume"]
        html = chain.run(resume=resume)
        with open("generated_portfolio.html", "w", encoding="utf-8") as f:
            f.write(html)
        return send_file("generated_portfolio.html", as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
