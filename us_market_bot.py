"""
매일 아침 7시(한국 시간) 미국 시황 리포트 생성 봇
Google Colab + Claude API 사용
"""

import os
import json
from datetime import datetime, timedelta
import requests
from anthropic import Anthropic

# ===================== 설정 =====================
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")  # 환경변수에서 불러오기
REPORT_DIR = "us_market_reports"  # 저장소 내 폴더

# ===================== 1. 시장 데이터 수집 =====================
def fetch_market_data():
    """
    미국 지수 & 뉴스 수집
    """
    market_data = {
        "timestamp": datetime.now().isoformat(),
        "note": "실제 데이터는 Claude가 웹 검색으로 수집합니다"
    }
    return market_data


def generate_report_with_claude():
    """
    Claude API를 사용해 미국 시황 리포트 생성
    """
    client = Anthropic()
    
    # 전일자 날짜 (미국 기준)
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Claude에 요청할 프롬프트
    system_prompt = """당신은 금융 분석가입니다.
매일 아침 미국 시장의 전일 시황을 분석하는 전문가입니다.
간결하고 인사이트 있는 리포트를 작성하세요."""
    
    user_prompt = f"""
{yesterday}(미국 현지 시간) 미국 주식시장 시황을 분석해주세요.

다음을 포함해주세요:
1. **주요 지수 현황**: S&P 500, NASDAQ, Dow Jones 종가 및 변동률
2. **시장 특징**: 어떤 섹터가 강했나? 약했나?
3. **주요 뉴스**: 시장에 영향을 미친 주요 소식 3-4개
4. **투자 인사이트**: 오늘 한국 시장에 미칠 영향

짧고 명확하게 작성하세요. (500자 이내)
"""
    
    print("🔄 Claude가 시황을 분석 중입니다...")
    
    try:
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        report_content = message.content[0].text
        return report_content
        
    except Exception as e:
        print(f"❌ Claude API 오류: {e}")
        return None


# ===================== 2. 리포트 저장 =====================
def save_report(content, date_str):
    """
    생성된 리포트를 마크다운으로 저장
    """
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    filename = f"{REPORT_DIR}/us_market_{date_str}.md"
    
    report_markdown = f"""# 📈 미국 시황 리포트
**생성일**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S (KST)")}
**분석대상**: {date_str}

---

## 📊 시장 분석

{content}

---

*자동 생성됨 | Claude API 기반*
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_markdown)
    
    print(f"✅ 리포트 저장됨: {filename}")
    return filename


# ===================== 3. 메인 실행 =====================
def main():
    """
    메인 실행 함수
    """
    print("=" * 50)
    print("🚀 미국 시황 봇 시작")
    print("=" * 50)
    
    # API Key 확인
    if not ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY 환경변수를 설정하세요")
        return
    
    # 리포트 생성
    report = generate_report_with_claude()
    
    if report:
        # 어제 날짜로 저장
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        save_report(report, yesterday)
        
        print("\n" + "=" * 50)
        print("📋 생성된 리포트:")
        print("=" * 50)
        print(report)
        print("=" * 50)
    else:
        print("❌ 리포트 생성 실패")


if __name__ == "__main__":
    main()
