from flask import Flask, render_template, request, jsonify
from universal_book.repository import UniversalBookRepository
from question_generator.generator import QuestionGenerator
from peer_platform.collaboration import PeerCollaborationPlatform
from progress_tracker.tracker import ProgressTracker
from ai_facilitator.facilitator import AIFacilitator
from knowledge_map.mapper import KnowledgeMapper

app = Flask(__name__, template_folder='templates')

book_repo = UniversalBookRepository()
question_gen = QuestionGenerator()
peer_platform = PeerCollaborationPlatform()
progress_tracker = ProgressTracker()
ai_facilitator = AIFacilitator()
knowledge_mapper = KnowledgeMapper()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/explore')
def explore():
    books = book_repo.get_random_books(5)
    return render_template('explore.html', books=books)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    books = book_repo.search_books(query)
    return render_template('search.html', books=books, query=query)


@app.route('/question', methods=['POST'])
def get_question():
    data = request.json
    book = None
    if 'book_id' in data:
        book = book_repo.get_book_by_id(data['book_id'])
    elif 'topic' in data:
        book = book_repo.get_book_by_title(data['topic'])

    if not book:
        return jsonify({'error': 'Book not found'}), 404

    try:
        questions = question_gen.generate_multiple_questions(book, n=3)
        return jsonify({'questions': questions})
    except Exception as e:
        app.logger.error(f"Error generating questions: {str(e)}")
        return jsonify({'error': 'An error occurred while generating questions'}), 500


@app.route('/peer_teach', methods=['POST'])
def peer_teach():
    lesson = request.json['lesson']
    peer_platform.submit_lesson(lesson)
    return jsonify({'status': 'success'})


@app.route('/track_progress', methods=['POST'])
def track_progress():
    goal = request.json['goal']
    progress = progress_tracker.update_progress(goal)
    return jsonify({'progress': progress})


@app.route('/facilitate', methods=['POST'])
def facilitate():
    context = request.json['context']
    prompt = ai_facilitator.generate_prompt(context)
    return jsonify({'prompt': prompt})


@app.route('/map_knowledge', methods=['POST'])
def map_knowledge():
    concepts = request.json['concepts']
    knowledge_map = knowledge_mapper.create_map(concepts)
    return jsonify({'map': knowledge_map})


if __name__ == '__main__':
    app.run(debug=True)
