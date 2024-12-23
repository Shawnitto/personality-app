from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# OpenAI API 키 설정
openai.api_key = "여기에_발급받은_API_키를_넣으세요"

def get_suggestions(personality, principle):
    # ChatGPT API 호출
    prompt = f"""
    성격: {personality}
    원칙: {principle}
    위의 성격과 원칙을 기반으로 어울리는 성향을 3~5개 추천해 주세요.
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-suggestions', methods=['POST'])
def suggest():
    data = request.get_json()
    personality = data.get('personality', '')
    principle = data.get('principle', '')
    suggestions = get_suggestions(personality, principle)
    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

    
