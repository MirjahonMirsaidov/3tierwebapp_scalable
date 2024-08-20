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

# Create a NAT gateway with an Elastic IP for each private subnet to get internet connectivity
resource "aws_eip" "gw" {
    count      = var.az_count
    domain = "vpc"
    depends_on = [aws_internet_gateway.prod_gw]
}

resource "aws_nat_gateway" "gw" {
    count         = var.az_count
    subnet_id     = element(aws_subnet.public.*.id, count.index)
    allocation_id = element(aws_eip.gw.*.id, count.index)
}


# Associate Subnet with Route Table
resource "aws_route_table_association" "a" {
    count          = var.az_count
    subnet_id      = element(aws_subnet.public.*.id, count.index)
    route_table_id = aws_route_table.prod_rt.id
}

# Create a new route table for the private subnets, make it route non-local traffic through the NAT gateway to the internet
resource "aws_route_table" "private" {
    count  = var.az_count
    vpc_id = aws_vpc.prod_vpc.id

    route {
        cidr_block     = "0.0.0.0/0"
        nat_gateway_id = element(aws_nat_gateway.gw.*.id, count.index)
    }
}

# Explicitly associate the newly created route tables to the private subnets (so they don't default to the main route table)
resource "aws_route_table_association" "private" {
    count          = var.az_count
    subnet_id      = element(aws_subnet.private.*.id, count.index)
    route_table_id = element(aws_route_table.private.*.id, count.index)
}
