resource "aws_vpc" "mtc_vpc" {
  cidr_block           = "10.123.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "derek-morgan-course-dev"
  }
}

resource "aws_subnet" "mtc_public_subnet" {
  vpc_id                  = aws_vpc.mtc_vpc.id
  cidr_block              = "10.123.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-west-2a"

  tags = {
    Name = "derek-morgan-course-dev-public"
  }
}

resource "aws_internet_gateway" "mtc_internet_gateway" {
  vpc_id = aws_vpc.mtc_vpc.id

  tags = {
    Name = "derek-morgan-course-dev-igw"
  }
}

resource "aws_route_table" "mtc_public_rt" {
  vpc_id = aws_vpc.mtc_vpc.id

  tags = {
    Name = "derek-morgan-course-dev-public-rt"
  }
}

resource "aws_route" "default_route" {
  route_table_id         = aws_route_table.mtc_public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.mtc_internet_gateway.id
}

resource "aws_route_table_association" "mtc_public_assoc" {
  subnet_id      = aws_subnet.mtc_public_subnet.id
  route_table_id = aws_route_table.mtc_public_rt.id
}

resource "aws_security_group" "mtc_sg" {
  name        = "derek-morgan-course-dev-public-sg"
  description = "public security group"
  vpc_id      = aws_vpc.mtc_vpc.id
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_key_pair" "mtc_auth" {
  key_name   = "derek-morgan-course-dev-mtckey"
  public_key = var.public_key
}

resource "aws_instance" "dev_node" {
  instance_type = "t2.micro"
  ami           = data.aws_ami.server_ami.id

  tags = {
    Name = "dev_node"
  }

  key_name               = aws_key_pair.mtc_auth.id
  vpc_security_group_ids = [aws_security_group.mtc_sg.id]
  subnet_id              = aws_subnet.mtc_public_subnet.id
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  user_data              = templatefile("userdata.tpl", {})

  root_block_device {
    volume_size = 8
  }

  # not necessary since we are going to run terraform from gh actions
  # provisioner "local-exec" {
  #   command = templatefile("windows-ssh-config.tpl", {
  #     hostname = self.public_ip,
  #     user     = "ubuntu",
  #   identityfile = "~/.ssh/derek-morgan-course-key" })
  #   interpreter = ["Powershell", "-Command"]
  # }
}

output "instance_public_ip" {
  value       = aws_instance.dev_node.public_ip
  description = "EC2 instance public ip. Use it to make requests to the DareData API."
}