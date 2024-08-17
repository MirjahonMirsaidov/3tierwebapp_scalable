# Create Security Groups
# Allow port 22, 80, 443 on EC2 instance
resource "aws_security_group" "allow_web_on_ec2" {
  name        = "allow_web"
  description = "Allow web access on EC2"
  vpc_id      = aws_vpc.prod_vpc.id

  tags = {
    Name = "allow_web"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_https" {
  security_group_id = aws_security_group.allow_web_on_ec2.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 443
  ip_protocol       = "tcp"
  to_port           = 443
}

resource "aws_vpc_security_group_ingress_rule" "allow_http" {
  security_group_id = aws_security_group.allow_web_on_ec2.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  ip_protocol       = "tcp"
  to_port           = 80
}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh" {
  security_group_id = aws_security_group.allow_web_on_ec2.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4" {
  security_group_id = aws_security_group.allow_web_on_ec2.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv6" {
  security_group_id = aws_security_group.allow_web_on_ec2.id
  cidr_ipv6         = "::/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}


# Create Network Interface with an ip in the Subnet created in step 4
resource "aws_network_interface" "prod_eni" {
  subnet_id       = aws_subnet.prod_us_east_1a_public.id
  private_ips     = ["10.0.0.50"]
  security_groups = [aws_security_group.allow_web_on_ec2.id]
}

# Assign Elastic ip to the Network Interface in step 7
resource "aws_eip" "prod_eip" {
  domain                    = "vpc"
  network_interface         = aws_network_interface.prod_eni.id
  associate_with_private_ip = "10.0.0.50"
  depends_on = [ aws_internet_gateway.prod_gw, aws_network_interface.prod_eni ]
}


# Create IAM Role
data "aws_iam_policy_document" "instance_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_policy" "s3_access" {
  name = "policy-381966"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["s3:*"]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_policy" "ecr_access" {
  name = "ecr-access-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}


resource "aws_iam_role" "prod_web_role" {
  name                = "prod_web_role"
  assume_role_policy  = data.aws_iam_policy_document.instance_assume_role_policy.json
  managed_policy_arns = [aws_iam_policy.s3_access.arn, aws_iam_policy.ecr_access.arn]
}

resource "aws_iam_instance_profile" "web_instance_profile" {
  name = "web_instance_profile"
  role = aws_iam_role.prod_web_role.name
}

# Create SSH key pair
resource "aws_key_pair" "my_key" {
  key_name   = "my-key-pair"
  public_key = file("${path.module}/ssh_key_pair.pub") # Path to your public key file
}


# Create EC2
resource "aws_instance" "web" {
  ami           = "ami-0c8e23f950c7725b9"
  instance_type = "t2.micro"
  availability_zone = "us-east-1a"
  iam_instance_profile = aws_iam_instance_profile.web_instance_profile.name
  root_block_device {
    encrypted = true
    volume_type = "gp3"
    volume_size = 20
  }
  key_name = aws_key_pair.my_key.key_name

  network_interface {
    network_interface_id = aws_network_interface.prod_eni.id
    device_index         = 0
  }

  user_data = file("${path.module}/user_data.sh")

  tags = {
    Name = "web"
  }
}
