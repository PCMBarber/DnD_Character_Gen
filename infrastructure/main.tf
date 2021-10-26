provider "aws" {
    region = var.region
    access_key = var.access_key
    secret_key = var.secret_key
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  token                  = data.aws_eks_cluster_auth.cluster.token
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.2.0"

  name                 = "dnd-vpc"
  cidr                 = "10.0.0.0/16"
  azs                  = ["eu-west-2a", "eu-west-2b", "eu-west-2c"]
  private_subnets      = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets       = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  database_subnets     = ["10.0.7.0/24", "10.0.8.0/24"]
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true
  create_database_nat_gateway_route = true
  create_database_subnet_group = true

  manage_default_security_group  = true
  default_security_group_name    = "pubgroup"
  default_security_group_ingress = [
    {
      from_port = 22,
      to_port = 22,
      cidr_blocks = "0.0.0.0/0"
      protocol = "tcp"
    }, 
    {
      from_port = 5000,
      to_port = 5000,
      cidr_blocks = "0.0.0.0/0"
      protocol = "tcp"
    },
    {
      from_port = 8080,
      to_port = 8080,
      cidr_blocks = "0.0.0.0/0"
      protocol = "tcp"
    },
  ]
  default_security_group_egress = [
    {
      from_port = 0,
      to_port = 0,
      cidr_blocks = "0.0.0.0/0"
    },
  ]
  tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  }

  public_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = local.cluster_name
  cluster_version = "1.20"
  subnets         = module.vpc.private_subnets

  tags = {
    Environment = "production"
  }

  vpc_id = module.vpc.vpc_id

  workers_group_defaults = {
    root_volume_type = "gp2"
  }

  worker_groups = [
    {
      name                          = "worker-group-1"
      instance_type                 = "t2.small"
      asg_desired_capacity          = 2
      additional_security_group_ids = [aws_security_group.worker_group_mgmt_one.id]
    },
    {
      name                          = "worker-group-2"
      instance_type                 = "t2.medium"
      additional_security_group_ids = [aws_security_group.worker_group_mgmt_two.id]
      asg_desired_capacity          = 1
    },
  ]
}

module "ec2" {
    source            = "./ec2"

    ami_id            = "ami-096cb92bb3580c759"
    instance_type     = "t2.medium"
    av_zone           = "eu-west-2a"
    key_name          = var.key_name
    sec_group_ids     = aws_security_group.rds.id
    subnet_group_name = module.vpc.database_subnet_group
    db_password       = var.db_password
    public_net_id     = element(module.vpc.public_subnets, 0)
    nat_ip            = element(module.vpc.nat_public_ips, 0)

    depends_on = [
      module.vpc
    ]
}

locals {
  cluster_name = "dnd-eks"
}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}
resource "random_string" "suffix" {
  length  = 8
  special = false
}