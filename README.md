# vllm-serve

VLLM serve with GPU VRAM monitoring stack

## Features

- **VLLM Inference Server**: Qwen/Qwen3-14B-AWQ 모델 서빙
- **GPU VRAM Monitoring**: NVIDIA DCGM Exporter를 통한 실시간 GPU 메모리 모니터링
- **Metrics Collection**: Prometheus를 통한 시계열 데이터 수집
- **Visualization**: Grafana 대시보드를 통한 시각화
- **System Monitoring**: Node Exporter를 통한 시스템 리소스 모니터링

## Quick Start

### 1. 환경 변수 설정
```bash
export MODEL=Qwen/Qwen3-14B-AWQ
export GPU_MEMORY_UTILIZATION=0.9
export MAX_NUM_SEQS=8
export MAX_MODEL_LEN=32768
```

### 2. Docker Compose 실행
```bash
docker-compose up -d
```

### 3. 모니터링 대시보드 접속
- **Grafana**: http://localhost:53000 (admin/admin)
- **Prometheus**: http://localhost:59090
- **VLLM API**: http://localhost:58000
- **VLLM Metrics**: http://localhost:58001/metrics
- **GPU Metrics**: http://localhost:59400/metrics

### 4. 테스트 실행
```bash
cd playground/feature-vllm-vram-monitoring
python test_vllm_monitoring.py
```

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│    VLLM     │    │     DCGM     │    │    Node     │
│  (GPU 추론)  │    │  (GPU 메트릭) │    │ (시스템 메트릭)│
└─────┬───────┘    └──────┬───────┘    └─────┬───────┘
      │                   │                   │
      │ metrics           │ metrics           │ metrics
      │ :8001             │ :9400             │ :9100
      │                   │                   │
      └───────────────────┼───────────────────┘
                          │
                    ┌─────▼─────┐
                    │Prometheus │
                    │   :9090   │
                    └─────┬─────┘
                          │ data
                    ┌─────▼─────┐
                    │  Grafana  │
                    │   :3000   │
                    └───────────┘
```

## Key Metrics

### GPU Metrics (DCGM)
- `DCGM_FI_DEV_FB_USED`: GPU 메모리 사용량
- `DCGM_FI_DEV_FB_TOTAL`: GPU 메모리 총량
- `DCGM_FI_DEV_GPU_UTIL`: GPU 사용률
- `DCGM_FI_DEV_GPU_TEMP`: GPU 온도
- `DCGM_FI_DEV_POWER_USAGE`: GPU 전력 사용량

### VLLM Metrics
- `vllm:num_requests_running`: 실행 중인 요청 수
- `vllm:num_requests_waiting`: 대기 중인 요청 수
- `vllm:num_requests_swapped`: 스왑된 요청 수

## Troubleshooting

### GPU 메트릭이 수집되지 않는 경우
```bash
# NVIDIA 드라이버 확인
nvidia-smi

# DCGM 컨테이너 로그 확인
docker logs dcgm-exporter
```

### VLLM 메트릭이 노출되지 않는 경우
```bash
# VLLM 컨테이너 로그 확인
docker logs vllm

# 메트릭 엔드포인트 직접 확인
curl http://localhost:58001/metrics
```
