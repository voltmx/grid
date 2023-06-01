resource "aws_ecs_cluster" "production" {
  name = "${var.ecs_cluster_name}-cluster"
}


resource "aws_ecs_task_definition" "app" {
  family = "django-app"
  container_definitions = templatefile("${path.module}/templates/django_app.json.tpl", {
    docker_image_url_django = var.docker_image_url_django
    region                  = var.region
  })
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs-execution-role.arn
  task_role_arn            = aws_iam_role.ecs-task-role.arn

}

resource "aws_ecs_service" "production" {
  name            = "${var.ecs_cluster_name}-service"
  cluster         = aws_ecs_cluster.production.id
  task_definition = aws_ecs_task_definition.app.arn
  depends_on      = [aws_alb_listener.ecs-alb-http-listener]
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    security_groups  = [aws_security_group.ecs.id]
    subnets          = [aws_subnet.private-subnet-1.id, aws_subnet.private-subnet-2.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.default-target-group.arn
    container_name   = "django-app"
    container_port   = 8000
  }
}
