# Create Security Groups
# Allow EC2 sg on Redis
resource "aws_security_group" "elasticache" {
  name        = "elasticache"
  description = "Allow EC2 access on Redis"
  vpc_id      = aws_vpc.prod_vpc.id

  tags = {
    Name = "elasticache"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_ec2_on_redis" {
  security_group_id = aws_security_group.elasticache.id
  referenced_security_group_id = aws_security_group.allow_web_on_ec2.id
  from_port         = 6379
  ip_protocol       = "tcp"
  to_port           = 6379
}


# Create Subnet group
resource "aws_elasticache_subnet_group" "prod" {
  name       = "prod"
  subnet_ids = [
    aws_subnet.prod_us_east_1a_private.id,
    aws_subnet.prod_us_east_1b_private.id
  ]

  tags = {
    Name = "Prod"
  }
}


# Create Redis Elasticache cluster
resource "aws_elasticache_cluster" "prod_redis" {
  cluster_id           = "prod-redis"
  engine               = "redis"
  node_type            = "cache.t4g.micro"
  num_cache_nodes      = 1
  engine_version       = "7.1"
  port                 = 6379
  subnet_group_name = aws_elasticache_subnet_group.prod.name
  security_group_ids = [aws_security_group.elasticache.id]
}
