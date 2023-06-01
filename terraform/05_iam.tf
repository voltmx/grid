resource "aws_iam_role" "ecs-execution-role" {
  name               = "ecs_execution_role_prod"
  assume_role_policy = file("policies/ecs-execution-role.json")
}

resource "aws_iam_role_policy_attachment" "ecs-task-execution-role-policy-attachment" {
  role       = aws_iam_role.ecs-execution-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ecs-task-role" {
  name               = "ecs_task_role_prod"
  assume_role_policy = file("policies/ecs-task-role.json")
}

resource "aws_iam_role_policy" "ecs-task-role-policy" {
  name   = "ecs_service_role_policy"
  policy = file("policies/ecs-task-role-policy.json")
  role   = aws_iam_role.ecs-task-role.id
}