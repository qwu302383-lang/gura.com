import os, zipfile

project_dir = os.path.dirname(os.path.abspath(__file__))
zip_filename = os.path.join(project_dir, "gura_cloud_deploy.zip")

exclude_names = {
    "__pycache__", ".env", "server.log", "public_url.txt", "cloudflared.exe",
    "cloudflared.EXE", ".git", ".gitignore", "gura_cloud_deploy.zip"
}
exclude_extensions = {".pyc", ".url"}

with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(project_dir):
        # filter dirs in place
        dirs[:] = [d for d in dirs if d not in exclude_names and not d.startswith(".")]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if file in exclude_names or ext in exclude_extensions:
                continue
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, project_dir)
            zf.write(abs_path, rel_path)

print(f"Deployment package created: {zip_filename} ({os.path.getsize(zip_filename)} bytes)")
