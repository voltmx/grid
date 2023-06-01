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
                    "hostPort": 8000,
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "environment": [
                {
                    "name": "SQL_USER",
                    "value": "postgres"
                },
                {
                    "name": "DJANGO_ALLOWED_HOSTS",
                    "value": "*"
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
                    "value": "django_dev"
                },
                {
                    "name": "SQL_PASSWORD",
                    "value": "buhb23CwCGxwSWrSPKdi"
                },
                {
                    "name": "SQL_HOST",
                    "value": "django-starter-db.cxkqq69wqv1a.us-west-1.rds.amazonaws.com"
                }
            ],
            "mountPoints": [],
            "volumesFrom": [],
            "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "/ecs/django-app",
                "awslogs-region": "${region}",
                "awslogs-stream-prefix": "django-app-log-stream"
            }
            }
        }
    ]