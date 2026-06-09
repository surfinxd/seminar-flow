variable "project_id" {
  type        = string
  description = "The GCP Project ID where resources will be provisioned"
  default     = "seminar-flow-project"
}

variable "region" {
  type        = string
  description = "The GCP Region for resources"
  default     = "asia-northeast3"
}

variable "zone" {
  type        = string
  description = "The GCP Zone for the GKE node pool"
  default     = "asia-northeast3-a"
}
