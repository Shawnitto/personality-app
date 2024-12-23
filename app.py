from flask import Flask, request, jsonify, render_template
import os
import openai

app = Flask(__name__)

# 환경 변수에서 OpenAI API 키 가져오기
openai.api_key = os.getenv('OPENAI_API_KEY')

# OpenAI API를 호출하는 함수
def get_suggestions(personality, principle):
    prompt = f"""
    성격: {personality}
    원칙: {principle}
    위의 성격과 원칙을 기반으로 적합한 성향을 추천해 주세요.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 최신 모델로 변경
            messages=[
                {"role": "system", "content": "You are an assistant that provides personality-based suggestions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"OpenAI API Error: {e}"

# 기본 라우팅 (홈페이지)
@app.route('/')
def home():
	return render_template('index.html')  # index.html 파일 렌더링

# 추천 결과를 반환하는 API
@app.route('/get-suggestions', methods=['POST'])
def suggest():
    if request.content_type == 'application/x-www-form-urlencoded':  # 폼 데이터 처리
        personality = request.form.get('personality', '')
        principle = request.form.get('principle', '')
    else:  # JSON 요청 처리
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415
        data = request.get_json()
        personality = data.get('personality', '')
        principle = data.get('principle', '')

    suggestions = get_suggestions(personality, principle)
    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
