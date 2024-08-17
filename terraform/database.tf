# Create Security Groups
# Allow EC2 sg on RDS
resource "aws_security_group" "allow_ec2_on_rds" {
  name        = "allow_ec2_on_rds"
  description = "Allow EC2 access on RDS"
  vpc_id      = aws_vpc.prod_vpc.id

  tags = {
    Name = "allow_ec2_on_rds"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_ec2" {
  security_group_id = aws_security_group.allow_ec2_on_rds.id
  referenced_security_group_id = aws_security_group.allow_web_on_ec2.id
  from_port         = 5432
  ip_protocol       = "tcp"
  to_port           = 5432
}


# Create Subnet group
resource "aws_db_subnet_group" "prod" {
  name       = "prod"
  subnet_ids = [
    aws_subnet.prod_us_east_1a_private.id,
    aws_subnet.prod_us_east_1b_private.id
  ]

  tags = {
    Name = "Prod"
  }
}


# Create RDS
resource "aws_db_instance" "wr_db" {
  identifier             = "wr"
  instance_class         = "db.t3.micro"
  allocated_storage      = 10
  engine                 = "postgres"
  engine_version         = "15.4"
  multi_az = false
  username               = var.db.username
  password               = var.db.password
  db_name = var.db.name
  availability_zone = "us-east-1a"
  db_subnet_group_name   = aws_db_subnet_group.prod.name
  vpc_security_group_ids = [aws_security_group.allow_ec2_on_rds.id]
  publicly_accessible    = false
  skip_final_snapshot    = true
}
