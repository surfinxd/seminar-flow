# 프로젝트: SeminarFlow (v2.0 - GitOps & CI/CD)

## 기술 스택
- **프레임워크/도구:** GitHub Actions, ArgoCD, Google Artifact Registry, Kubernetes(GKE), Terraform (IaC), Sealed Secrets (by Bitnami)
- **배포 방식:** Kustomize 또는 Helm (다중 환경 지원용)

## 아키텍처 규칙
- CRITICAL: 클러스터의 상태는 무조건 Git 저장소의 매니페스트와 일치해야 함 (Single Source of Truth)
- CRITICAL: `Rolling Update` 전략과 `Readiness Probe`를 반드시 적용하여 배포 시 트래픽 유실을 방지할 것
- CRITICAL: 모든 민감 정보(DB 비밀번호, JWT 비밀 키 등)는 평문으로 매니페스트에 노출해서는 안 되며, 반드시 Sealed Secrets(`SealedSecret`)를 통해 암호화한 후 Git 저장소에 커밋되어야 함

## 환경 분리 프로세스
- CRITICAL: **GitOps 기반 환경 분리 (Dev vs Prod)**
  - ArgoCD와 Kustomize(또는 Helm Values)를 활용하여 `k8s/overlays/dev`와 `k8s/overlays/prod`로 환경을 분리합니다.
  - **Dev 환경:** 기능 브랜치 Merge 시 즉시 배포되며, 작은 리소스 할당량을 가집니다.
  - **Prod 환경:** Main 브랜치의 특정 태그 릴리스 시에만 배포되며, 운영 수준의 리소스 할당량을 적용합니다.

## 개발 프로세스
- CRITICAL: 애플리케이션 코드를 수정하여 Git에 푸시하면, 수동 배포 없이 GitHub Actions를 통해 Google Artifact Registry에 자동 빌드/푸시 되어야 함
- `v1.0`의 TDD 원칙을 CI 파이프라인에 통합하여, 테스트 실패 시 빌드가 중단되도록 구성할 것

## 명령어
- **가상환경 설정 (로컬 테스트용):** `python -m venv venv && source venv/bin/activate`
- **CI 파이프라인 트리거:** `git push origin main`
- **ArgoCD 동기화 강제 실행:** `argocd app sync seminar-flow-dev`
- **GCP 인프라 프로비저닝 (Terraform):**
  - 테라폼 초기화: `cd v2.0/terraform && terraform init`
  - 인프라 변경계획 확인: `terraform plan -var="project_id=YOUR_PROJECT_ID"`
  - 인프라 반영 및 빌드: `terraform apply -var="project_id=YOUR_PROJECT_ID"`
- **Sealed Secrets 암호화 실행 (kubeseal CLI):**
  - 평문 시크릿 파일 암호화:
    `kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system --format yaml < secret-plain.yaml > v2.0/k8s/overlays/dev/sealed-secret.yaml`
  - 리터럴로부터 바로 암호화된 SealedSecret 생성:
    `kubectl create secret generic seminar-flow-secrets --from-literal=postgres-password="PASSWORD" --from-literal=secret-key="JWT_KEY" --from-literal=database-url="postgresql+psycopg2://postgres:PASSWORD@postgresql:5432/seminar_flow" --dry-run=client -o yaml | kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system --format yaml > v2.0/k8s/overlays/dev/sealed-secret.yaml`
