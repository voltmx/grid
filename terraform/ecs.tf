resource "aws_ecs_cluster" "production" {
  name = "${var.ecs_cluster_name}-cluster"
}


resource "aws_ecs_task_definition" "app" {
  family = "django-app"
  container_definitions = templatefile("${path.module}/templates/django_app.json.tpl", {
    docker_image_url_django     = var.docker_image_url_django
    docker_image_url_nginx      = var.docker_image_url_nginx
    region                      = var.region
    rds_db_name                 = var.rds_db_name
    rds_username                = var.rds_username
    rds_password                = var.rds_password
    rds_hostname                = aws_db_instance.production.address
    django_allowed_hosts        = var.django_allowed_hosts
    django_csrf_trusted_origins = var.django_csrf_trusted_origins
    sqs_access_key              = aws_iam_access_key.da_celery_sqs.id
    sqs_secret_key              = aws_iam_access_key.da_celery_sqs.secret
  })
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs-execution-role.arn
  task_role_arn            = aws_iam_role.ecs-task-role.arn
  depends_on               = [aws_db_instance.production]
  volume {
    name = "static_volume"
  }
}

resource "aws_ecs_service" "da_web_app" {
  name                   = "${var.ecs_cluster_name}-web-service"
  cluster                = aws_ecs_cluster.production.id
  task_definition        = aws_ecs_task_definition.app.arn
  depends_on             = [aws_alb_listener.ecs-alb-http-listener]
  desired_count          = 1
  launch_type            = "FARGATE"
  enable_execute_command = true
  network_configuration {
    security_groups  = [aws_security_group.ecs.id]
    subnets          = [aws_subnet.private-subnet-1.id, aws_subnet.private-subnet-2.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.default-target-group.arn
    container_name   = "nginx"
    container_port   = 80
  }
}

resource "aws_ecs_task_definition" "celery_worker" {
  family = "celery-worker"
  container_definitions = templatefile("${path.module}/templates/celery_worker.json.tpl", {
    docker_image_url_django     = var.docker_image_url_django
    region                      = var.region
    rds_db_name                 = var.rds_db_name
    rds_username                = var.rds_username
    rds_password                = var.rds_password
    rds_hostname                = aws_db_instance.production.address
    django_allowed_hosts        = var.django_allowed_hosts
    django_csrf_trusted_origins = var.django_csrf_trusted_origins
    sqs_access_key              = aws_iam_access_key.da_celery_sqs.id
    sqs_secret_key              = aws_iam_access_key.da_celery_sqs.secret
  })
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs-execution-role.arn
  task_role_arn            = aws_iam_role.ecs-task-role.arn
  depends_on               = [aws_db_instance.production]
  volume {
    name = "static_volume"
  }
}


resource "aws_ecs_service" "da_celery" {
  name                   = "${var.ecs_cluster_name}-celery-service"
  cluster                = aws_ecs_cluster.production.id
  task_definition        = aws_ecs_task_definition.celery_worker.arn
  depends_on             = [aws_alb_listener.ecs-alb-http-listener]
  desired_count          = 1
  launch_type            = "FARGATE"
  enable_execute_command = true
  network_configuration {
    security_groups  = [aws_security_group.ecs.id]
    subnets          = [aws_subnet.private-subnet-1.id, aws_subnet.private-subnet-2.id]
    assign_public_ip = false
  }
}



resource "aws_ecs_task_definition" "celery_beat" {
  family = "celery-beat"
  container_definitions = templatefile("${path.module}/templates/celery_beat.json.tpl", {
    docker_image_url_django     = var.docker_image_url_django
    region                      = var.region
    rds_db_name                 = var.rds_db_name
    rds_username                = var.rds_username
    rds_password                = var.rds_password
    rds_hostname                = aws_db_instance.production.address
    django_allowed_hosts        = var.django_allowed_hosts
    django_csrf_trusted_origins = var.django_csrf_trusted_origins
    sqs_access_key              = aws_iam_access_key.da_celery_sqs.id
    sqs_secret_key              = aws_iam_access_key.da_celery_sqs.secret
  })
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs-execution-role.arn
  task_role_arn            = aws_iam_role.ecs-task-role.arn
  depends_on               = [aws_db_instance.production]
  volume {
    name = "static_volume"
  }
}


resource "aws_ecs_service" "da_celery_beat" {
  name                   = "${var.ecs_cluster_name}-celery-beat-service"
  cluster                = aws_ecs_cluster.production.id
  task_definition        = aws_ecs_task_definition.celery_beat.arn
  depends_on             = [aws_alb_listener.ecs-alb-http-listener]
  desired_count          = 1
  launch_type            = "FARGATE"
  enable_execute_command = true
  network_configuration {
    security_groups  = [aws_security_group.ecs.id]
    subnets          = [aws_subnet.private-subnet-1.id, aws_subnet.private-subnet-2.id]
    assign_public_ip = false
  }
}





