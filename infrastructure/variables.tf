variable "access_key" {
    type = string
    sensitive = true
}
variable "secret_key" {
    type = string
    sensitive = true
}
variable "db_password" {
    type = string
    sensitive = true
}
variable "region" {
  default     = "eu-west-2"
  description = "AWS region"
}
variable "key_name" {
  default     = "terraforminit"
  description = "instance SSH key"
}
variable "docker_user" {
  default     = "stratcastor"
  description = "instance SSH key"
}