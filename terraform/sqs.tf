resource "aws_sqs_queue" "da-celery" {
  name                      = "da-celery-queue"
  receive_wait_time_seconds = 10
}

resource "aws_iam_user" "da_celery_sqs" {
  name = "da-celery-sqs-user"
}

resource "aws_iam_user_policy" "da_celery_sqs" {
  user = aws_iam_user.da_celery_sqs.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sqs:*",
        ]   
        Effect   = "Allow"
        Resource = "arn:aws:sqs:*:*:*"
      },
    ]
  })
}

resource "aws_iam_access_key" "da_celery_sqs" {
  user = aws_iam_user.da_celery_sqs.name
}
