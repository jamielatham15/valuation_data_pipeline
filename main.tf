terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-0022f774911c1d690"
  instance_type = "t2.micro"

  tags = {
    Name = "valuation_data_pipeline"
  }
}

resource "aws_ecr_repository" "app_container_registry" {
  name                 = "app_container_registry"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "valuation_data_pipeline"
  }
}

/*
resource "aws_db_instance" "app_db" {
  allocated_storage = 20
  engine = "postgres"
  engine_version = "14.2"
  instance_class = "db.t3.micro"

  tags = {
    Name = "valuation_data_pipeline"
  }
}
*/