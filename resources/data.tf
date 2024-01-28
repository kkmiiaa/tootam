
resource "null_resource" "tootam-exporter-pip-install" {
    provisioner "local-exec" {
        command = "pip install -r ../lambda/tootam-exporter/source/requirements.txt -t ../lambda/tootam-exporter/source"
    }
}

data "archive_file" "tootam-exporter" {
    depends_on = ["null_resource.tootam-exporter-pip-install"]
    type        = "zip"
    source_dir  = "../lambda/tootam-exporter/source"
    output_path = "../lambda/tootam-exporter/source.zip"
}

