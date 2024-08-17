# Create S3 bucket
resource "aws_s3_bucket" "prod_bucket" {
  bucket = "mirjahon-aws-s3"
  force_destroy = true

  tags = {
    Name        = "mirjahon-aws-s3"
  }
}
