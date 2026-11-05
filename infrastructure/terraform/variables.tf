variable "aws_region" {
  description = "AWS region for all NuriVoyage resources."
  type        = string
  default     = "eu-north-1"
}

variable "aws_profile" {
  description = "Local AWS CLI profile used for provisioning."
  type        = string
  default     = "HoldMyCoffee"
}

variable "environment" {
  type    = string
  default = "production"
}

variable "vpc_id" {
  description = "Existing VPC for the EC2 host."
  type        = string
}

variable "subnet_id" {
  description = "Existing subnet for the EC2 host. Use a public subnet only when an approved HTTPS edge is available."
  type        = string
}

variable "ami_id" {
  description = "x86_64 Amazon Linux 2023 AMI in aws_region."
  type        = string
}

variable "instance_type" {
  type    = string
  default = "t3.small"
}

variable "allowed_ingress_cidr_blocks" {
  description = "CIDR blocks allowed to reach HTTP/HTTPS. Keep empty until an approved edge or office CIDR is available."
  type        = list(string)
  default     = []
}

variable "ecr_repository_name" {
  type    = string
  default = "nurivoyage"
}
