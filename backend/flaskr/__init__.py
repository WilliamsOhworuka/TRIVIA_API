import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import and_, func
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, collection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10

    current_collection = collection[start:end]
    questions = [question.format() for question in current_collection]
    return (questions, len(collection))


def format_categories(unformatted_categories):
    categories = {}

    for category in unformatted_categories:
        categories.update(category.format())

    return categories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        unformatted_categories = Category.query.all()

        return jsonify({
            'success': True,
            'categories': format_categories(unformatted_categories)
        })

    @app.route('/questions')
    def get_questions():
        (questions, total_questions) = paginate_questions(
            request, Question.query.order_by(Question.id).all())
        unformatted_categories = Category.query.all()

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'categories': format_categories(unformatted_categories),
            'total_questions': total_questions,
            'current_category': 0
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            (questions, total_questions) = paginate_questions(
                request, Question.query.order_by(Question.id).all())

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': questions,
                'total_questions': total_questions
            })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        if search_term:
            results = Question.query.filter(
                Question.question.ilike((f'%{search_term}%'))).all()
            (questions, total_questions) = paginate_questions(request, results)

            return jsonify({
                'success': True,
                'current_category': 0,
                'questions': questions,
                'total_questions': total_questions,
            })

        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)

        if not question or not answer or not difficulty or not category:
            abort(400)

        try:
            new_question = Question(
                question=question, answer=answer, difficulty=difficulty, category=category)
            new_question.insert()
            (questions, total_questions) = paginate_questions(
                request, Question.query.order_by(Question.id).all())

            return jsonify({
                'success': True,
                'created': new_question.id,
                'questions': questions,
                'total_questions': total_questions
            })

        except:
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        (questions, total_questions) = paginate_questions(
            request, Question.query.filter(Question.category == category_id).order_by(Question.id).all())

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': total_questions,
            'current_category': category_id
        })

    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        is_array = isinstance(previous_questions, list)

        if not is_array or not quiz_category:
            abort(400)

        next_question = Question.query.filter(~Question.id.in_(previous_questions)).order_by(
            func.random()).first()

        if int(quiz_category['id']):
            next_question = Question.query.filter(and_(Question.category == quiz_category['id'], ~Question.id.in_(previous_questions))).order_by(
                func.random()).first()

        next_question = next_question.format() if next_question else None

        return jsonify({
            'success': True,
            'question': next_question
        })

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(425)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 425,
            'message': 'Method Not Allowed'
        }), 425

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app
