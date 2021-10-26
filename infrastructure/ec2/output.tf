output "bastion_ip" {
  value = aws_instance.bastion.public_ip
}
output "jenk_ip" {
  value = aws_instance.jenkins.public_ip
}
output "db_ip" {
  value = element(split(":",aws_db_instance.DnD.endpoint),0)
}