resource "aws_instance" "discordradiobot" {
  ami           = "ami-04681163a08179f28"
  instance_type = "t2.micro"

  # The user_data property uses a shell script to install Docker and run your Discord bot container.
  user_data = file("bootstrap.sh")

  tags = {
    Name = "Discord-Bot-Instance"
  }
}