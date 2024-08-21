output "db_endpoint" {
  value = aws_db_instance.wr_db.endpoint
}

output "cache_endpoint" {
  value = "${aws_elasticache_cluster.prod_redis.cache_nodes.0.address}:${aws_elasticache_cluster.prod_redis.cache_nodes.0.port}"
}
