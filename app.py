from flask import Flask, render_template, request, send_file
from langchain.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

app = Flask(__name__)

prompt = PromptTemplate(
    input_variables=["resume"],
    template=open("prompt.txt").read()
)

llm = ChatOllama(model="llama3:8b-instruct")
chain = LLMChain(llm=llm, prompt=prompt)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume = request.form["resume"]
        html = chain.run(resume=resume)
        with open("generated_portfolio.html", "w") as f:
            f.write(html)
        return send_file("generated_portfolio.html", as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

