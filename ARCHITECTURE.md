# 아키텍처 (v2.0: GitOps & CI/CD)

## 디렉토리 구조
```text
v2.0/
├── .github/
│   └── workflows/
│       └── ci-cd.yaml
├── app/
├── argocd/
│   └── application.yaml
├── k8s/
│   ├── base/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── postgresql.yaml
│   └── overlays/
│       ├── dev/
│       │   ├── kustomization.yaml
│       │   └── sealed-secret.yaml
│       └── prod/
│           ├── kustomization.yaml
│           └── sealed-secret.yaml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── providers.tf
│   └── outputs.tf
└── Dockerfile
```

## 패턴
- **Infrastructure as Code (IaC) 패턴:** 테라폼을 이용하여 GCP 인프라(VPC, 서브넷, GKE, Node Pool, Google Artifact Registry)를 선언적 코드로 구성하여 인프라 형상 관리 및 손쉬운 재생성 보장
- **GitOps 배포 패턴:** Git 저장소를 단일 진실 공급원(Single Source of Truth)으로 삼아, 클러스터의 상태를 Git과 동일하게 유지
- **Sealed Secrets 패턴:** 데이터베이스 비밀번호, JWT 비밀 키와 같은 민감한 보안 정보를 공개 Git 저장소에 안전하게 커밋하기 위해 비대칭 암호화를 거친 `SealedSecret` 커스텀 리소스로 관리하고, 클러스터 내 컨트롤러가 감지하여 일반 Kubernetes `Secret`으로 복호화하는 보안 패턴
- **Rolling Update 패턴:** 애플리케이션 업데이트 시, 기존 Pod를 유지한 채로 새 Pod를 띄우고(Readiness Probe 확인 후) 점진적으로 트래픽을 전환하여 무중단 배포 달성

## 데이터 흐름
1. **CI 파이프라인:** 개발자 GitHub Push ➡️ GitHub Actions (테스트 및 빌드) ➡️ Docker 이미지 Google Artifact Registry Push
2. **CD 파이프라인:** 이미지 태그 업데이트 ➡️ ArgoCD 감지 ➡️ GCP GKE 클러스터 상태 동기화 및 무중단 배포 진행
3. **보안 정보 복호화 흐름:** ArgoCD가 `SealedSecret` 리소스를 GKE 클러스터에 배포 ➡️ 클러스터 내부의 Sealed Secrets Controller가 감지 ➡️ 클러스터 내부의 마스터 Private Key로 이를 복호화하여 일반 `Secret` 생성 ➡️ FastAPI 및 PostgreSQL Pod가 `secretKeyRef`를 통해 복호화된 실제 환경변수 값을 안전하게 주입받아 구동
4. **트래픽 흐름:** v1.0과 동일하게 애플리케이션 동작
