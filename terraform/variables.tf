variable "aws_region" {
  description = "AWS region created in"
  type        = string
  default     = "us-east-1"
}

variable "ec2_ami" {
  description = "AMI ID used for the EC2 instance"
  type        = string
  default     = "ami-04681163a08179f28"
}