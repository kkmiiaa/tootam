resource "aws_iam_policy" "tootam-exporter" {
  name        = "tootam-exporter-logging-policy"
  path        = "/"
  description = "IAM policy for logging from a tootam-exporter"

  policy = jsonencode(
    {
      "Statement" : [
        {
          "Action" : "logs:CreateLogGroup",
          "Effect" : "Allow",
          "Resource" : "arn:aws:logs:ap-northeast-1:269671422737:*"
        },
        {
          "Action" : [
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          "Effect" : "Allow",
          "Resource" : [
            "arn:aws:logs:ap-northeast-1:269671422737:log-group:/aws/lambda/tootam-exporter:*"
          ]
        }
      ],
      "Version" : "2012-10-17"
    }
  )
}

resource "aws_iam_role" "tootam-exporter" {
  name = "tootam-exporter-execution-role"
  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : "sts:AssumeRole",
          "Principal" : {
            "Service" : "lambda.amazonaws.com"
          },
          "Effect" : "Allow",
          "Sid" : ""
        }
      ]
    }
  )

  managed_policy_arns = [
    aws_iam_policy.tootam-exporter.arn,
  ]
}