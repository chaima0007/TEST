# Caelum Partners — Vector Store Infrastructure (Weaviate Cloud)
# Apply: terraform init && terraform plan && terraform apply
# Requires: WEAVIATE_API_KEY, WEAVIATE_CLUSTER_URL env vars

terraform {
  required_providers {
    weaviate = {
      source  = "weaviate/weaviate"
      version = "~> 2.0"
    }
  }
}

provider "weaviate" {
  scheme  = "https"
  host    = var.weaviate_cluster_url
  api_key = var.weaviate_api_key
}

variable "weaviate_cluster_url" {
  description = "Weaviate cluster URL (from Weaviate Cloud Console)"
  type        = string
}

variable "weaviate_api_key" {
  description = "Weaviate API key"
  type        = string
  sensitive   = true
}

resource "weaviate_class" "knowledge_base" {
  class       = "KnowledgeBase"
  description = "Caelum Partners KB — companies, personas, playbooks"
  vectorizer  = "text2vec-openai"

  properties = [
    { name = "content", data_type = ["text"] },
    { name = "category", data_type = ["text"] },
    { name = "slug", data_type = ["text"] },
    { name = "language", data_type = ["text"] },
    { name = "last_updated", data_type = ["date"] },
  ]
}
