output "alb_hostname" {
  value = aws_lb.production.dns_name
}

output "dkim_values" {
  value = aws_ses_domain_dkim.domain_dkim.dkim_tokens
}

output "identity_values" {
  value = aws_ses_domain_identity.domain_identity.verification_token
}

