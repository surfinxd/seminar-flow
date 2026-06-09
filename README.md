# SeminarFlow v2.0 (GitOps & CI/CD)

SeminarFlow 프로젝트의 두 번째 버전(v2.0)입니다.
v1.0의 수동 배포 환경에서 겪었던 한계를 극복하기 위해 v1.0의 핵심 애플리케이션 코드를 유지한 상태로, GitOps 아키텍처(ArgoCD 및 Kustomize)와 CI/CD 자동화 파이프라인(GitHub Actions)을 구축하여 Google Cloud Platform (GCP) 환경에 무중단 자동화 배포를 구현했습니다.

## 🛠 아키텍처 및 기술 스택
- **프레임워크:** FastAPI
- **언어:** Python 3.11+
- **데이터베이스:** PostgreSQL (SQLAlchemy ORM 사용)
- **설계 패턴:** Controller - Service - Repository 로 분리된 **3-Tier Architecture**
- **인프라:** Docker, Kubernetes (Kustomize 기반 환경 분리), Google Artifact Registry (GAR), Google Kubernetes Engine (GKE), Terraform (IaC)
- **CI/CD 및 GitOps:** GitHub Actions, ArgoCD, Sealed Secrets (보안 정보 암호화 및 선언적 관리)

## ✨ 주요 기능

### 1. 사용자 인증 (JWT & Local Auth)
- Local ID 및 Password 기반의 회원가입과 로그인을 지원합니다.
- `passlib` 및 `python-jose`를 활용하여 비밀번호를 안전하게 단방향 암호화(Bcrypt)하고, 서비스 내 API 접근 시 JWT(JSON Web Token)를 이용한 인증을 수행합니다.

### 2. 세미나 도메인 및 예약 (동시성 제어)
- 주최자가 세미나 정보를 등록하고 참여자가 목록 및 상세 정보를 조회합니다.
- 선착순 예약 시 발생하는 트래픽 스파이크 상황에서 정원 초과 오류를 방지하기 위해 **Pessimistic Locking (`SELECT ... FOR UPDATE`)** 기법을 적용하여 데이터 무결성을 보장합니다.

### 3. 무중단 배포 및 롤링 업데이트 (Rolling Update)
- 애플리케이션 업데이트 시 기존 Pod를 유지한 채 새 Pod를 기동하는 `Rolling Update` 전략을 구현했습니다.
- `Readiness Probe`와 `Liveness Probe`를 활용한 헬스 체크, 그리고 `preStop` 훅(5초 sleep)을 통해 기존 요청을 안전하게 처리한 뒤 파드를 교체함으로써 트래픽 유실 없는 무중단 배포를 지원합니다.

## 📖 API 문서 (API Specification)
- 상세한 API 엔드포인트 명세, 요청/응답 형식, 그리고 에러 상황에 대한 문서는 [API.md](file:///Users/dxlee/Documents/seminar-flow/v1.0/API.md)에서 확인할 수 있습니다.
- 서버 구동 시 Swagger UI (`/docs`) 또는 ReDoc (`/redoc`) 주소를 통해 대화형 API 테스트를 지원합니다.

## 🚀 실행 및 테스트 방법

### 1. 로컬 개발 및 테스트
v2.0 코드는 TDD 원칙을 준수하여 작성되었으며, 기능 수정 후 아래 명령어를 통해 정상 동작 여부를 즉시 확인할 수 있습니다.

```bash
# 1. 프로젝트 디렉토리 이동 및 가상환경 생성/활성화
cd v2.0
python -m venv venv
source venv/bin/activate  # Windows의 경우: venv\Scripts\activate

# 2. 의존성 패키지 설치
pip install -r requirements.txt
pip install pytest httpx

# 3. 로컬 서버 실행 (테스트 목적)
uvicorn app.main:app --reload

# 4. 전체 테스트(TDD) 실행 (DB 동시성 제어 및 JWT 인증 검증 포함)
pytest
```

### 2. GitOps 및 CI/CD 배포 과정
로컬 검증이 완료된 코드는 GitOps 모델에 따라 자동으로 클러스터에 배포됩니다.

1. **코드 커밋 및 푸시 (배포 트리거)**
   `main` 브랜치에 코드를 커밋하고 푸시합니다.
   ```bash
   git add .
   git commit -m "feat: 세미나 예약 동시성 제어 로직 추가"
   git push origin main
   ```

2. **자동화 파이프라인 동작 (GitHub Actions)**
   - 푸시 시 GitHub Actions가 작동하여 테스트(`pytest`)를 자동으로 수행합니다.
   - 테스트 성공 시 Google Artifact Registry(GAR)에 Docker 이미지를 빌드 및 푸시합니다.
   - Kustomize 파일(`k8s/overlays/dev/kustomization.yaml`)의 이미지 태그를 최신 SHA로 자동 갱신한 뒤 Git 저장소에 커밋합니다.

3. **지속적 배포 및 클러스터 동기화 (ArgoCD)**
   - ArgoCD가 Git 저장소의 매니페스트 변경을 감지하고 GKE 클러스터에 배포를 동기화합니다.
   - 롤링 업데이트(Rolling Update) 전략을 사용하므로 무중단으로 새 버전이 배포됩니다.
   - 필요 시 아래 명령어로 강제 동기화하여 즉시 반영할 수 있습니다.
     ```bash
     argocd app sync seminar-flow-dev
     ```

### 3. GCP 인프라 프로비저닝 (Terraform)
코드로 정의된 GCP 인프라를 프로비저닝하려면 아래 단계를 수행합니다.

```bash
# 1. 테라폼 디렉토리 이동 및 초기화
cd v2.0/terraform
terraform init

# 2. 인프라 계획 확인 및 반영 (본인의 GCP 프로젝트 ID 지정 필요)
terraform plan -var="project_id=YOUR_GCP_PROJECT_ID"
terraform apply -var="project_id=YOUR_GCP_PROJECT_ID"
```

### 4. 보안 정보 암호화 및 관리 (Sealed Secrets)
SeminarFlow는 GitOps 배포 환경에서 데이터베이스 패스워드, JWT 비밀 키와 같은 민감 정보를 안전하게 선언적 코드로 관리하기 위해 **Sealed Secrets**를 활용합니다.
민감 정보는 `kubeseal` CLI를 이용해 로컬에서 암호화한 후 `SealedSecret` 리소스로 Git에 안전하게 커밋할 수 있습니다.

#### [1] kubeseal CLI 설치
로컬 운영체제에 맞게 CLI 도구를 설치합니다:
```bash
# macOS
brew install kubeseal

# Windows (Chocolatey)
choco install kubeseal
```

#### [2] 보안 정보 생성 및 암호화 절차
보안 정보를 새로 등록하거나 변경하려면 GKE 클러스터의 Sealed Secrets 컨트롤러 인증서를 사용하여 아래와 같이 암호화합니다:

```bash
# dev 환경용 SealedSecret 생성 예시
kubectl create secret generic seminar-flow-secrets \
  --from-literal=postgres-password="YOUR_DB_PASSWORD" \
  --from-literal=secret-key="YOUR_JWT_SECRET_KEY" \
  --from-literal=database-url="postgresql+psycopg2://postgres:YOUR_DB_PASSWORD@postgresql:5432/seminar_flow" \
  --dry-run=client -o yaml | \
  kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system --format yaml \
  > v2.0/k8s/overlays/dev/sealed-secret.yaml

# prod 환경용 SealedSecret 생성 예시
kubectl create secret generic seminar-flow-secrets \
  --from-literal=postgres-password="YOUR_PROD_DB_PASSWORD" \
  --from-literal=secret-key="YOUR_PROD_JWT_SECRET_KEY" \
  --from-literal=database-url="postgresql+psycopg2://postgres:YOUR_PROD_DB_PASSWORD@postgresql:5432/seminar_flow" \
  --dry-run=client -o yaml | \
  kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system --format yaml \
  > v2.0/k8s/overlays/prod/sealed-secret.yaml
```

*참고: 생성된 `sealed-secret.yaml` 파일은 비대칭 암호화가 적용되어 Git 저장소에 평문 노출 없이 안전하게 푸시하여 배포할 수 있습니다.*



## 📦 GitOps 및 CI/CD 배포 (자동)
수동 배포의 한계를 극복하고 자동화된 무중단 배포 흐름을 위해 다음 구성요소들이 세팅되어 있습니다.
- `terraform/`: VPC Network, Subnet, GKE Cluster, Node Pool, Google Artifact Registry, Service Account 및 IAM 권한 설정을 자동 프로비저닝하기 위한 Terraform 구성 파일들
- `.github/workflows/ci-cd.yaml`: GitHub Actions를 통한 CI(TDD 검증) 및 CD(Google Artifact Registry 빌드/푸시 및 Dev 환경 매니페스트 이미지 태그 자동 갱신) 파이프라인
- `k8s/base`: 무중단 배포를 위한 `deployment.yaml`(Probes 및 preStop 적용, Secret 기반 환경변수 매핑), `service.yaml`, `postgresql.yaml`(Secret 기반 패스워드 매핑) 공통 매니페스트
- `k8s/overlays/dev`: 개발 환경 전용 Kustomize 패치 및 `sealed-secret.yaml` (접두사 `dev-`, 태그 자동 갱신, dev용 암호화 보안 변수 설정)
- `k8s/overlays/prod`: 운영 환경 전용 Kustomize 패치 및 `sealed-secret.yaml` (접두사 `prod-`, 3개 레플리카 확장, `stable` 태그, prod용 암호화 보안 변수 설정)
- `argocd/application.yaml`: GKE 클러스터 상태와 Git 저장소의 `v2.0/k8s/overlays/dev` 경로 동기화(Automated Sync)를 담당하는 ArgoCD 매니페스트
