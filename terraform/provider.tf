terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Reference an Existing VPC
data "aws_vpc" "discordradiobotex" {
  # Filter by the Name/ id
  filter {
    name   = "tag:Name"
    values = ["VPC1"] # VPC's Name tag
  }
}

# Output the VPC ID (optional, for debugging or confirmation)
output "vpc-03ac619faa1c682ca" {
  value = data.aws_vpc.discordradiobotex.id
}