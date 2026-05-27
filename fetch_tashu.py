import requests
import json
import os
from datetime import datetime

API_KEY = os.environ.get('TASHU_API_KEY')
if not API_KEY:
    raise ValueError('TASHU_API_KEY가 설정되지 않았습니다.)
URL = 'https://bikeapp.tashu.or.kr:50041/v1/openapi/station'

headers = {
    'api-token': API_KEY,
    'Accept': 'application/json'
}

try:
    res = requests.get(URL, headers=headers, timeout=10)
    data = res.json()
    stations = data.get('results', [])

    seogu = []
    for s in stations:
        lat = float(s.get('x_pos', 0))
        lng = float(s.get('y_pos', 0))
        if 36.28 <= lat <= 36.38 and 127.32 <= lng <= 127.42:
            seogu.append({
                'id': s.get('id'),
                'name': s.get('name'),
                'lat': lat,
                'lng': lng,
                'parking': s.get('parking_count', 0)
            })

    output = {
        'updated_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
        'count': len(seogu),
        'stations': seogu
    }

    with open('seogu_realtime.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f'완료: 서구 {len(seogu)}개 대여소')

except Exception as e:
    print(f'오류: {e}')
    # 오류 시 빈 파일 생성 (HTML이 오류 안 나도록)
    with open('seogu_realtime.json', 'w') as f:
        json.dump({'updated_at': 'error', 'count': 0, 'stations': []}, f)
