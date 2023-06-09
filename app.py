import os

from paperswithcode import PapersWithCodeClient
from flask import Flask, request, jsonify, send_file, Response

app = Flask(__name__)

# define the api endpoint for the main content of the plugin
@app.route('/papers', methods=['GET'])
def get_papers():
    topic = request.args.get('topic')
    total_papers = request.args.get('total_papers')
    client = PapersWithCodeClient()
    papers = client.paper_list(q = topic, items_per_page=total_papers)

    if papers.count == 0:
        return jsonify({'error': "No papers found! It is possible that either I can't find the papers or there is a typo in the topic."})
    response_papers = []
    for paper in papers.results:
        response_papers.append({
            "title": paper.title,
            "summary": paper.abstract,
            "pdf": paper.url_pdf,
            "abs_pdf": paper.url_abs
        })
    return jsonify({"count": len(response_papers), "papers": response_papers})


# Define the API endpoint for the plugin logo
@app.route('/logo.png', methods=['GET'])
def plugin_logo():
    file_path = os.path.join("assets", "logo.jfif")
    return send_file(file_path, mimetype='image/jfif')

# Define the API endpoint for the plugin manifest
@app.route('/ai-plugin.json', methods=['GET'])
def plugin_manifest():
    host = request.headers['Host']
    with open("ai-plugin.json") as f:
        text = f.read()
        return Response(text, mimetype='text/json')

# Define the API endpoint for the OpenAPI specification
@app.route('/openapi.yaml', methods=['GET'])
def openapi_spec():
    host = request.headers['Host']
    with open('./openapi.yaml') as f:
        text = f.read()
        return Response(text, mimetype='text/yaml')
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

