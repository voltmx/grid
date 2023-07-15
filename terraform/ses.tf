resource "aws_ses_domain_identity" "domain_identity" {
  domain = var.domain
}

resource "aws_ses_domain_dkim" "domain_dkim" {
  domain = aws_ses_domain_identity.domain_identity.domain
}

resource "aws_iam_user" "smtp_user" {
  name = "smtp_user"
}

# User for sending email through SES SMTP
resource "aws_iam_access_key" "smtp_user" {
  user = aws_iam_user.smtp_user.name
}

resource "aws_iam_user_policy" "ses_sender_user_policy" {
  name = "ses_sender"
  user = aws_iam_user.smtp_user.name

  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ses:SendRawEmail",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}
