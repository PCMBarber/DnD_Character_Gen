output "bastion_ip" {
  value = aws_instance.bastion.public_ip
}
output "jenk_ip" {
  value = aws_instance.jenkins.public_ip
}