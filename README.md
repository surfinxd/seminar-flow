# SeminarFlow v2.0 (GitOps & CI/CD)

SeminarFlow 프로젝트의 두 번째 버전(v2.0)입니다.
v1.0의 수동 배포 환경에서 겪었던 한계를 극복하기 위해 핵심 애플리케이션 코드를 유지한 상태로, GitOps 아키텍처(ArgoCD 및 Kustomize)와 CI/CD 자동화 파이프라인(GitHub Actions)을 구축하여 Google Cloud Platform (GCP) 환경에 무중단 자동화 배포를 구현했습니다.

---

## 🛠 아키텍처 및 기술 스택
- **프레임워크:** FastAPI (Python 3.11+)
- **데이터베이스:** PostgreSQL (SQLAlchemy ORM 사용)
- **설계 패턴:** Controller - Service - Repository 로 분리된 **3-Tier Architecture**
- **인프라:** Docker, Kubernetes (Kustomize 기반 환경 분리), Google Artifact Registry (GAR), Google Kubernetes Engine (GKE), Terraform (IaC)
- **CI/CD 및 GitOps:** GitHub Actions, ArgoCD, Sealed Secrets (보안 정보 암호화 및 선언적 관리)

---

## ✨ v2.0 핵심 개선 기능
1. **CI/CD 파이프라인 자동화**: 코드를 GitHub에 Push하면 자동으로 테스트(`pytest`)를 거쳐 도커 이미지를 빌드하여 Google Artifact Registry(GAR)에 적재하고, Kustomize 이미지 태그를 자동 갱신 및 Git 재커밋을 수행합니다.
2. **선언적 GitOps 배포**: ArgoCD가 Git의 이미지 태그 변화를 실시간으로 감지하고 GKE 클러스터에 배포(Auto-Sync)하여 동기화 상태를 유지합니다.
3. **보안 정보 선언적 관리**: 데이터베이스 비밀번호, JWT 비밀 키 등의 민감 정보를 GKE Sealed Secrets를 통해 암호화된 매니페스트(`sealed-secret.yaml`) 형태로 Git에서 선언적으로 안전하게 관리합니다.
4. **무중단 롤링 업데이트**: `Readiness Probe`와 `preStop` 훅을 활용한 Graceful Shutdown 및 트래픽 점진적 분산으로 배포 도중 발생할 수 있는 5xx 에러 및 트래픽 누락을 원천 차단합니다.

---

## 📖 핵심 개발 및 운영 문서 가이드 (docs/)
v2.0 프로젝트의 구축, 실행 및 트러블슈팅에 대한 세부 사항은 다음 문서들을 참고하세요.

* **[docs/execution_guide.md](docs/execution_guide.md)**: GCP 설정, Terraform 기반 인프라 구축, GKE 자격 증명 및 Sealed Secrets, ArgoCD GitOps 적용까지의 단계별 전체 실행 가이드라인
* **[docs/secret_management.md](docs/secret_management.md)**: 프로젝트 내 식별된 보안 민감 정보(GCP SA Key, DB 비밀번호, JWT 키 등)의 위험성 분석 및 생명주기별 안전한 주입 가이드라인
* **[docs/iam-binding-description.md](docs/iam-binding-description.md)**: Terraform 인프라 구축 과정에서 최소 권한 정책(Least Privilege)에 따라 할당되는 GCP IAM 역할(Role) 및 서비스 계정(SA) 매핑 명세서
* **[docs/troubleshooting.md](docs/troubleshooting.md)**: ArgoCD 연동 에러, Sealed Secrets 복호화 실패, DB 호스트명 해석 불능 등 실제 구축 과정에서 발생한 에러 기록 및 해결 이력
* **[docs/v2.0_measurement_report.md](docs/v2.0_measurement_report.md)**: GKE 환경에서 수동 배포 대비 GitOps 배포 시간 단축율 및 k6 부하 테스트 도중 트래픽 무손실 성능을 입증한 실측 결과 보고서

---

## 📦 프로젝트 디렉토리 구조
```text
├── .github/workflows/   # GitHub Actions CI/CD 워크플로우 (TDD 검증, 도커 빌드/푸시, 태그 업데이트)
├── app/                 # FastAPI 애플리케이션 소스 코드 (auth, seminars, reservations)
├── argocd/              # ArgoCD Application 선언 매니페스트 (application.yaml)
├── docs/                # v2.0 아키텍처 가이드라인, 트러블슈팅, 성능 측정 보고서
├── k8s/
│   ├── base/            # 공통 Kubernetes 매니페스트 (deployment, service, postgresql)
│   └── overlays/
│       ├── dev/         # 개발 환경 Kustomize 패치 및 dev용 암호화 시크릿 (sealed-secret.yaml)
│       └── prod/        # 운영 환경 Kustomize 패치 (3개 Replica 확장, prod용 암호화 시크릿)
├── terraform/           # GCP VPC, GKE, GAR 및 IAM 자동 프로비저닝을 위한 Terraform IaC 코드
└── tests/               # Pytest 기반 통합 및 단위 테스트 코드
```
