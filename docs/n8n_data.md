Current configuration
In your docker-compose.yml, the n8n service uses a bind mount:
volumes:  - ./n8n_data:/home/node/.n8n
This maps the local ./n8n_data directory to the container's data directory, so data is stored on your host filesystem, not inside the container.
What this means
Workflows persist when you:
Stop containers (docker compose stop)
Restart containers (docker compose restart)
Remove containers (docker compose rm or docker compose down without -v)
Workflows are lost if you:
Delete the n8n_data folder manually
Use docker compose down -v (this removes named volumes, but since you're using a bind mount, it shouldn't affect n8n_data)
Verify persistence
Check that n8n_data exists:
   ls -la n8n_data/
You should see files like database.sqlite, config, etc.
After stopping and restarting:
   docker compose down   docker compose up -d n8n
Your workflows should still be there when you access http://localhost:5678.
Recommendation: add to .gitignore
Since n8n_data/ contains runtime data and potentially sensitive configuration, consider adding it to .gitignore:
# n8n data directory n8n_data/
This prevents committing large binary files and sensitive data. If you want to version control workflows, export them as JSON files instead.
Backup strategy
For extra safety, you can:
Export workflows as JSON from the n8n UI (workflow → three dots → "Download")
Back up the n8n_data folder periodically:
   tar -czf n8n_data_backup_$(date +%Y%m%d).tar.gz n8n_data/
Your current setup should preserve workflows across container restarts. The bind mount ensures data lives on your host filesystem, not in ephemeral container storage.