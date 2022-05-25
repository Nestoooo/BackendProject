import json

from fastapi import FastAPI, Request, Response, Form
import requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import database
import random
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")
#table = database.create_table()
#database.drop_table()


# extract a response of questions from api request
def process_response(quiz_json):
    print(" >>> ", process_response.__name__)
    # list of questions dictionary to send to html
    function_response = []
    for x in range(4):
        # dictionary to hold question plus answers
        function_response_dic = {"question": "", "answers": ""}
        response_incorrect_answers = []
        all_choices = []

        response_question = quiz_json[x]["question"]
        function_response_dic["question"] = response_question
        #########
        response_correct_answer = quiz_json[x]["correctAnswer"]
        response_incorrect_answers = quiz_json[x]["incorrectAnswers"]
        all_choices = response_incorrect_answers
        all_choices.append(response_correct_answer)
        random.shuffle(all_choices)
        function_response_dic["answers"] = all_choices
        #########
        function_response.append(function_response_dic)
    return function_response

# extract a response of questions from api request
def process_correct_answers(quiz_json):
    print(" >>> ", process_correct_answers.__name__)
    # list of questions dictionary to send to html
    response = []
    for x in range(4):
        correct_answer = quiz_json[x]["correctAnswer"]
        response.append(correct_answer)
    return response

# open a web page for all quizes
@app.api_route("/", response_class=HTMLResponse, methods=['GET', 'POST','DELETE'])
def all_quizes(request: Request):
    print(" >>> ", all_quizes.__name__)

    # using API to request a quiz
    if request.method == "POST":
        print(" >>> ", all_quizes.__name__, " POST")
        url = requests.get("https://the-trivia-api.com/api/questions?categories=food_and_drink&limit=4&difficulty=easy")
        respo_json = url.json()

        # counter to concatenate to the quiz name
        counter = database.count_quizes()
        counter = str(counter)

        # convert full quiz response from json (list(dictionary)) format, to string
        respo_str = json.dumps(respo_json)

        # add full quiz response (as string) to the database
        try:
            database.add_quiz('Quiz ' + counter, respo_str)
        except:
            print("insert in progress ...")

        # get all quizes from the database
        try:
            getting_all = database.get_all()
        except:
            print("get all error!")
        return templates.TemplateResponse("all_quizes.html", {"request": request, "response": getting_all})

    if request.method == "GET":
        print(" >>> ", all_quizes.__name__, " GET")
        # get all quizes from the database
        try:
            getting_all = database.get_all()
        except:
            print("get all error!")
        return templates.TemplateResponse("all_quizes.html", {"request": request, "response": getting_all})


#to delete quiz
@app.api_route("/del_{quiz_name}", response_class=HTMLResponse, methods=['GET', 'POST'])
def remove_quiz(request: Request, quiz_name: str):
    print(" >>> ", remove_quiz.__name__)
    delete_quiz = database.delete_quiz(quiz_name)
    #return templates.TemplateResponse("all_quizes.html", {"request": request, "quiz_name": quiz_name})
    return quiz_name+" deleted!"

# open a web page for the quiz
@app.api_route("/quiz/{quiz_name}", response_class=HTMLResponse, methods=['GET', 'POST'])
def quiz(request: Request, quiz_name: str):
    print(" >>> ", quiz.__name__)
    # get quiz data using the quiz name
    retrieve_quiz_data = database.get_quiz(quiz_name)
    # convert full quiz response back to its original json format (from list(tuple(list(dictionaries))) to list(dictionaries) )
    retrieve_quiz_data = retrieve_quiz_data[0][0]
    retrieve_quiz_json = json.loads(retrieve_quiz_data)
    # extract a response as list of (question, answers) from the full quiz response json
    function_response = process_response(retrieve_quiz_json)
    global correct_answers
    correct_answers = process_correct_answers(retrieve_quiz_json)

    return templates.TemplateResponse("quiz.html", {"request": request, "response": function_response, "quiz_name": quiz_name})

#result of quiz answered and the score
@app.api_route("/solve/{quiz_name}", response_class=HTMLResponse, methods=['GET', 'POST'])
async def solve_quiz(request: Request, answers: list = Form(...)):
    print(" >>> ", solve_quiz.__name__)
    score = 0
    for x in range(4):
        if answers[x] == correct_answers[x]:
            score = score + 1

    return templates.TemplateResponse("solve.html", {"request": request, "response": answers, "correct_answers": correct_answers, "score": score})



