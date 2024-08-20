# ECR repo
resource "aws_ecr_repository" "wr" {
  name = "wr"
  force_delete = true
}
