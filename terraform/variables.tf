
variable "postgres_user" {
  type    = string
  default = "cloudops"
}

variable "postgres_password" {
  type      = string
  sensitive = true
}

variable "postgres_db" {
  type    = string
  default = "cloudops"
}
