output "jenk_ip" {
    value = module.ec2.jenk_ip
}
output "cluster_endpoint" {
  description = "Endpoint for EKS control plane."
  value       = module.eks.cluster_endpoint
}
output "config_map_aws_auth" {
  description = "A kubernetes configuration to authenticate to this EKS cluster."
  value       = module.eks.config_map_aws_auth
}
output "cluster_security_group_id" {
  description = "Security group ids attached to the cluster control plane."
  value       = module.eks.cluster_security_group_id
}
output "region" {
  description = "AWS region"
  value       = var.region
}
output "cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = local.cluster_name
}
output "DB_Public_IP" {
  description = "RDS Instance Public IP"
  value       = module.ec2.db_ip
} 