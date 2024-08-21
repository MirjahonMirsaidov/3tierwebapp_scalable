# Fetch AZs in the current region
data "aws_availability_zones" "available" {
  state = "available"
}


# Create VPC
resource "aws_vpc" "prod_vpc" {
  cidr_block       = "10.0.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "prod_vpc"
  }
}


# Create Subnets
resource "aws_subnet" "public" {
  count = var.az_count
  cidr_block = cidrsubnet(aws_vpc.prod_vpc.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  vpc_id     = aws_vpc.prod_vpc.id

  tags = {
    Name = "public"
  }
}


resource "aws_subnet" "private" {
  count = var.az_count
  cidr_block = cidrsubnet(aws_vpc.prod_vpc.cidr_block, 8, var.az_count + count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  vpc_id     = aws_vpc.prod_vpc.id

  tags = {
    Name = "private"
  }
}


# Create Internet Gateway
resource "aws_internet_gateway" "prod_gw" {
  vpc_id = aws_vpc.prod_vpc.id

  tags = {
    Name = "prod_gw"
  }
}


# Create Route Table
resource "aws_route_table" "prod_rt" {
  vpc_id = aws_vpc.prod_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.prod_gw.id
  }

  route {
    ipv6_cidr_block        = "::/0"
    gateway_id = aws_internet_gateway.prod_gw.id
  }

  tags = {
    Name = "prod_rt"
  }
}


# Associate Subnet with Route Table
resource "aws_route_table_association" "a" {
    count          = var.az_count
    subnet_id      = element(aws_subnet.public.*.id, count.index)
    route_table_id = aws_route_table.prod_rt.id
}
