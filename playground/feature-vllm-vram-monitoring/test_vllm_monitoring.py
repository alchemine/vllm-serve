#!/usr/bin/env python3
"""
VLLM VRAM 모니터링 테스트 스크립트
Docker Compose로 실행된 모니터링 스택을 테스트합니다.
"""

import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

def test_prometheus_endpoints():
    """Prometheus 메트릭 엔드포인트들을 테스트합니다."""
    endpoints = {
        "Prometheus": "http://localhost:59090/api/v1/targets",
        "Node Exporter": "http://localhost:59100/metrics",
        "VLLM Metrics": "http://localhost:58000/metrics",
        "Grafana": "http://localhost:53000/api/health"
    }
    
    print("=== 모니터링 엔드포인트 상태 확인 ===")
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=5)
            status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
            print(f"{name:15}: {status}")
        except Exception as e:
            print(f"{name:15}: ❌ Error - {str(e)[:50]}")

def test_vllm_inference():
    """VLLM 추론을 실행해서 GPU 사용량을 증가시킵니다."""
    llm_server_url = "http://localhost:58000/v1"
    llm = ChatOpenAI(
        openai_api_key="EMPTY",
        openai_api_base=llm_server_url,
        model_name="Qwen/Qwen3-14B-AWQ",
        temperature=0.7,
        max_tokens=100,
    )
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "{input}")
    ])
    
    test_queries = [
        "안녕하세요! 오늘 날씨가 어떤가요?",
        "Python에서 GPU 메모리를 모니터링하는 방법을 알려주세요.",
        "머신러닝 모델의 성능을 최적화하는 방법은 무엇인가요?",
    ]
    
    print("\n=== VLLM 추론 테스트 시작 ===")
    for i, query in enumerate(test_queries, 1):
        try:
            input_prompt = prompt_template.invoke({"input": query})
            print(f"테스트 {i}: {query[:30]}...")
            response = llm.invoke(input_prompt)
            print(f"응답: {response.content[:50]}...")
            time.sleep(2)  # GPU 사용량 확인을 위한 대기
        except Exception as e:
            print(f"테스트 {i} 실패: {e}")

def main():
    """메인 테스트 함수"""
    print("VLLM VRAM 모니터링 시스템 테스트")
    print("=" * 50)
    
    # 엔드포인트 상태 확인
    test_prometheus_endpoints()
    
    # VLLM 추론 테스트 (GPU 사용량 증가)
    test_vllm_inference()
        
    print("\n=== 테스트 완료 ===")
    print("Grafana 대시보드: http://localhost:53000 (admin/admin)")
    print("Prometheus: http://localhost:59090")
    print("VLLM 서버: http://localhost:58000")

if __name__ == "__main__":
    main()