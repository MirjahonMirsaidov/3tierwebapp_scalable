# ecs.tf

resource "aws_ecs_cluster" "main" {
    name = "cb-cluster"
}

resource "aws_ecs_task_definition" "app" {
    family                   = "cb-app-task"
    task_role_arn = aws_iam_role.ecs_task_role.arn
    execution_role_arn       = "arn:aws:iam::381492290017:role/ecsTaskExecutionRole"
    network_mode             = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    cpu                      = var.fargate_cpu
    memory                   = var.fargate_memory
    container_definitions    = jsonencode([{
    environment = []
    name            = "cb-app"
    image           = aws_ecr_repository.wr.repository_url
    pu                      = tonumber(var.fargate_cpu)
    memory                   = tonumber(var.fargate_memory)
    networkMode     = "awsvpc"
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = "/ecs/cb-app"
        awslogs-region        = "us-east-1"
        awslogs-stream-prefix = "ecs"
      }
    }
    portMappings = [{
      containerPort = var.app_port
      hostPort      = var.app_port
    }]
  }])
}

resource "aws_ecs_service" "main" {
    name            = "cb-service"
    cluster         = aws_ecs_cluster.main.id
    task_definition = aws_ecs_task_definition.app.arn
    desired_count   = var.app_count
    launch_type     = "FARGATE"

    network_configuration {
        security_groups  = [aws_security_group.ecs_tasks.id]
        subnets          = aws_subnet.private.*.id
        assign_public_ip = true
    }

    load_balancer {
        target_group_arn = aws_alb_target_group.app.id
        container_name   = "cb-app"
        container_port   = var.app_port
    }

    depends_on = [aws_alb_listener.front_end]
}
