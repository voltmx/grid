[
  {
    "name": "django-app",
    "image": "${docker_image_url_django}",
    "cpu": 10,
    "memory": 512,
    "portMappings": [
      {
        "name": "django-app-8000-tcp",
        "containerPort": 8000,
        "protocol": "tcp"
      }
    ],
    "essential": true,
    "environment": [
      {
        "name": "DJANGO_ALLOWED_HOSTS",
        "value": "${django_allowed_hosts}"
      },
      {
        "name": "DJANGO_CSRF_TRUSTED_ORIGINS",
        "value": "${django_csrf_trusted_origins}"
      },
      {
        "name": "SQL_USER",
        "value": "${rds_username}"
      },
      {
        "name": "SQL_PORT",
        "value": "5432"
      },
      {
        "name": "SECRET_KEY",
        "value": "BERRSECRET123123123"
      },
      {
        "name": "SQL_DATABASE",
        "value": "${rds_db_name}"
      },
      {
        "name": "SQL_PASSWORD",
        "value": "${rds_password}"
      },
      {
        "name": "SQL_HOST",
        "value": "${rds_hostname}"
      }
    ],
    "mountPoints": [
      {
        "containerPath": "/app/staticfiles",
        "sourceVolume": "static_volume"
      }
    ],
    "volumesFrom": [],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/django-app",
        "awslogs-region": "${region}",
        "awslogs-stream-prefix": "django-app-log-stream"
      }
    }
  },
  {
    "name": "nginx",
    "image": "${docker_image_url_nginx}",
    "essential": true,
    "cpu": 10,
    "memory": 128,
    "portMappings": [
      {
        "containerPort": 80,
        "protocol": "tcp"
      }
    ],
    "mountPoints": [
      {
        "containerPath": "/app/staticfiles",
        "sourceVolume": "static_volume"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/nginx",
        "awslogs-region": "${region}",
        "awslogs-stream-prefix": "nginx-log-stream"
      }
    }
  }
]
