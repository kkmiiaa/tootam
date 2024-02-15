resource "aws_cloudwatch_log_group" "tootam-exporter" {
  name              = "/aws/lambda/tootam-exporter"
  retention_in_days = 7
}

resource "aws_lambda_function" "tootam-exporter" {
  filename         = data.archive_file.tootam-exporter.output_path
  function_name    = "tootam-exporter"
  role             = aws_iam_role.tootam-exporter.arn
  handler          = "main.lambda_handler"
  runtime          = "python3.12"
  source_code_hash = data.archive_file.tootam-exporter.output_base64sha256
}