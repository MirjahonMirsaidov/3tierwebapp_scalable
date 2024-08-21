
# Import github iam role
resource "aws_iam_role" "ecr_access_github_role" {
  name = "ECRAccessGithubRole"
  lifecycle {
    prevent_destroy = true
  }

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Federated = "arn:aws:iam::381492290017:oidc-provider/token.actions.githubusercontent.com"
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
          },
          StringLike = {
            "token.actions.githubusercontent.com:sub": "repo:MirjahonMirsaidov/*"
          }
        }
      }
    ]
  })
}


# Attach Amazon ECR full access managed policy
resource "aws_iam_role_policy_attachment" "ecr_access_github_role_ecr_policy" {
  role       = aws_iam_role.ecr_access_github_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess"
}

# Attach Amazon ECS full access managed policy
resource "aws_iam_role_policy_attachment" "ecr_access_github_role_ecs_policy" {
  role       = aws_iam_role.ecr_access_github_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonECS_FullAccess"
}


# Attach IAM Policy for github iam role
resource "aws_iam_policy" "ecr_access_policy" {
  name        = "ECRAccessPolicy"
  description = "Provides ECR access and PassRole permissions"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Action = "iam:PassRole",
        Resource = "arn:aws:iam::381492290017:role/web-server-role"
      }
    ]
  })
}

# Attach the policy to the ECRAccessGithubRole
resource "aws_iam_role_policy_attachment" "ecr_access_policy_attachment" {
  role       = "ECRAccessGithubRole"
  policy_arn = aws_iam_policy.ecr_access_policy.arn
}


# ECS Task Role
resource "aws_iam_role" "ecs_task_role" {
  name = "web-server-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Effect   = "Allow"
        Sid      = ""
      }
    ]
  })
}

# Attach a Policy to the Role to Allow Full Access to a Specific S3 Bucket
resource "aws_iam_role_policy" "ecs_task_s3_policy" {
  name   = "ecsTaskS3Policy"
  role   = aws_iam_role.ecs_task_role.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:s3:::mirjahon-aws-s3",
          "arn:aws:s3:::mirjahon-aws-s3/*"
        ]
      }
    ]
  })
}

data "aws_iam_policy_document" "ecs_auto_scale_role" {
  version = "2012-10-17"
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["application-autoscaling.amazonaws.com"]
    }
  }
}

# ECS auto scale role
resource "aws_iam_role" "ecs_auto_scale_role" {
  name               = var.ecs_auto_scale_role_name
  assume_role_policy = data.aws_iam_policy_document.ecs_auto_scale_role.json
}

# ECS auto scale role policy attachment
resource "aws_iam_role_policy_attachment" "ecs_auto_scale_role" {
  role       = aws_iam_role.ecs_auto_scale_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceAutoscaleRole"
}
