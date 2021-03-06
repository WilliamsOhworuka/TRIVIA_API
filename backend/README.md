# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Reference
### Getting started
- Base URL: The app can only be run locally as it has not been hosted as a base url. The backend is hosted at ```http://127.0.0.1:5000```.

### Error Handling
Errors are return as JSON objects in the following format
```
{
    "success": False,
    "error": 400,
    "message": 'bad request'
}
```
The endpoints will return three types of errors when request fails;
- 400: Bad request
- 404: Resource Not found
- 422: unprocessable

### Endpoints
```
GET '/categories'
GET '/questions'
GET '/categories/<int:category_id>/questions'
POST '/questions'
POST '/quizzes'
DELETE '/questions/<int:question_id>'
```

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
- Sample: ```curl http://127.0.0.1:5000/categories```
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

GET '/questions'
- Fetches a dictionary in which the keys are questions, categories, total_questions and current_category
- Request Argument: page number
- Results are parginated in groups of 10. include a request argument to choose page number starting from 1.
- Returns: An object with keys;
     questions: a list of question objects. categories: an object with key:value pairs of id and category type.
     total_questions: total number of questions.  current_category: category id of the current category.

- Sample: ```curl http://127.0.0.1:5000/questions?page=1```
```
{
    'success': True,
    'questions': [{
        'id': 1,
        'question': 'what is my name',
        'answer': 'Williams',
        'category': '1',
        'difficulty': 3
    },
    {
        'id': 2,
        'question': 'what year is this',
        'answer': '2019,
        'category': '1',
        'difficulty': 2
    }],
    'categories': {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    },
    'total_questions': 2,
    'current_category': 1
}
```

DELETE '/questions/<int:question_id>'
- Deletes a particular question 
- Request Argument: question_id
- Returns: An object with keys;
     deleted: the id of deleted question.
     questions: array of the remaining qustions.
     total_questions: total number of questions.
- Sample: ```curl -X DELETE http://127.0.0.1/questions/1```
```
{
    'success': True,
    'deleted': 1,
    'questions': [
    {
        'id': 2,
        'question': 'what year is this',
        'answer': '2019,
        'category': '1',
        'difficulty': 2
    }],
    'total_questions': 1
}
```

POST '/questions'
- creates a new question using the submitted question, answer, difficulty and category.  
- Request Argument: None
- Returns: An object with keys;
     created: the id of deleted question.
     questions: array of the current qustions.
     total_questions: total number of questions.
- Sample: ```curl http://127.0.0.1/questions -X POST -H "Content-type: application/json" -d '{"question": 'What is my name', "answer": 'Mario', "difficulty":1, "category":1}'```
```
{
    'success': True,
    'created': 3,
    'questions': [
    {
        'id': 2,
        'question': 'what year is this',
        'answer': '2019,
        'category': '1',
        'difficulty': 2
    },
    {
        'id': 3,
        'question': 'what is my name',
        'answer': 'mario',
        'category': '1',
        'difficulty': 1
    }],
    'total_questions': 2
}
```

POST '/questions'
- fetches a list of questions that match the search string submitted.  
- Request Argument: None
- Results are parginated in groups of 10. include a request argument to choose page number starting from 1.
- Returns: An object with keys;
     current_category: the id of the current category.
     questions: array of questions.
     total_questions: total number of questions.
- Sample: ```curl http://127.0.0.1/questions -X POST -H "Content-type: application/json" -d '{"searchTerm": 'What'}'```
```
{
    'success': True,
    'questions': [
    {
        'id': 2,
        'question': 'what year is this',
        'answer': '2019,
        'category': '1',
        'difficulty': 2
    },
    {
        'id': 3,
        'question': 'what is my name',
        'answer': 'mario',
        'category': '1',
        'difficulty': 1
    }],
    'total_questions': 2,
    'current_category': 0
}
```

GET '/categories/<int:category_id>/questions'
- fetches a list of questions for a particular category.
- Request Argument: category_id, page number
- Results are parginated in groups of 10. include a request argument to choose page number starting from 1.
- Returns: An object with keys;
     current_category: the id of the current category.
     questions: array of questions.
     total_questions: total number of questions.
- Sample: ```curl http://127.0.0.1/categories/1/questions?page=1```
```
{
    'success': True,
    'questions': [
    {
        'id': 2,
        'question': 'what year is this',
        'answer': '2019,
        'category': '1',
        'difficulty': 2
    },
    {
        'id': 3,
        'question': 'what is my name',
        'answer': 'mario',
        'category': '1',
        'difficulty': 1
    }],
    'total_questions': 2,
    'current_category': 1
}
```

POST '/quizzes'
- fetches a random question that is not part of the list of previous questions submitted from the selected category.
- Request Argument: None
- Returns: An object with keys;
     question: a random question object.
- Sample: ```curl http://127.0.0.1/quizzes -X POST -H "Content-type: application/json" -d '{"previous_questions": [1], "quiz_category": {"id":1,"type": 'science'}}'```
```
{
    'success': True,
    'question': {
        'id': 3,
        'question': 'what is my name',
        'answer': 'mario',
        'category': '1',
        'difficulty': 1
    }
}
```




## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```