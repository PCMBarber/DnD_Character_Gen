resource "aws_instance" "jenkins" {
  ami                         = var.ami_id 
  instance_type               = var.instance_type 
  availability_zone           = var.av_zone 
  key_name                    = var.key_name
  subnet_id                   = var.public_net_id
  associate_public_ip_address = true
  user_data                   = "${file("user_data_kubectl.sh")}"

  tags = {
    Name = "jenkins"
  }
}

resource "aws_instance" "bastion" {
  ami                         = var.ami_id 
  instance_type               = var.instance_type 
  availability_zone           = var.av_zone 
  key_name                    = var.key_name
  subnet_id                   = var.public_net_id
  associate_public_ip_address = true
  user_data                   = "${file("user_data_ansible.sh")}"

  tags = {
    Name = "bastion"
  }
}

resource "aws_db_instance" "DnD" {
  identifier             = "dnd"
  name                   = "DnD"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "mysql"
  engine_version         = "5.7"
  username               = "root"
  password               = var.db_password
  db_subnet_group_name   = var.subnet_group_name
  vpc_security_group_ids = var.sec_group_ids
  parameter_group_name   = "default.mysql5.7"
  publicly_accessible    = false
  skip_final_snapshot    = true
}