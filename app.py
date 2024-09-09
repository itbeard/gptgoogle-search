import logging
from flask import Flask, render_template, request, jsonify
from search_service import SearchService
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

search_service = SearchService(app.config['TAVILY_API_KEY'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    results_per_page = 10  # Changed from 15 to 10

    if not query:
        return jsonify({'error': 'Empty search query'}), 400
    
    if len(query) < 3:
        return jsonify({'error': 'Search query must be at least 3 characters long'}), 400

    try:
        results = search_service.search(query, max_results=50)  # Request 50 results
        if not results:
            logger.warning(f"No results found for query: {query}")
            return render_template('results.html', 
                                   query=query, 
                                   results=[], 
                                   page=1, 
                                   total_pages=1,
                                   error="No results found. Please try a different search query.")

        total_results = len(results)
        start_index = (page - 1) * results_per_page
        end_index = start_index + results_per_page
        paginated_results = results[start_index:end_index]

        return render_template('results.html', 
                               query=query, 
                               results=paginated_results, 
                               page=page, 
                               total_pages=(total_results + results_per_page - 1) // results_per_page)
    except Exception as e:
        logger.error(f"Error processing search request: {str(e)}")
        return render_template('results.html', 
                               query=query, 
                               results=[], 
                               page=1, 
                               total_pages=1,
                               error="An error occurred while processing your request. Please try again later.")

if __name__ == '__main__':
    app.run(debug=True)