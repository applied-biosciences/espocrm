output "ecr_repository_url" { value = aws_ecr_repository.app.repository_url }
output "release_bucket_name" { value = aws_s3_bucket.release.bucket }
output "ec2_instance_id" { value = aws_instance.app.id }
output "security_group_id" { value = aws_security_group.app.id }
output "app_private_ip" { value = aws_instance.app.private_ip }
