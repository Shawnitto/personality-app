from flask import Flask, request, jsonify
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
    위의 성격과 원칙을 기반으로 어울리는 성향을 3~5개 추천해 주세요.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # 적절한 엔진 선택
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"OpenAI API Error: {e}"

# Flask 라우팅
@app.route('/get-suggestions', methods=['POST'])
def suggest():
    # 요청이 JSON인지 확인
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415  # 415: Unsupported Media Type
    
    # 요청 데이터 가져오기
    data = request.get_json()
    personality = data.get('personality', '')
    principle = data.get('principle', '')

    # OpenAI API를 호출해 추천 결과 생성
    suggestions = get_suggestions(personality, principle)

    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render에서 제공한 PORT 환경 변수 사용
    app.run(host='0.0.0.0', port=port, debug=True)
