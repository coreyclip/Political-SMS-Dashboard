EXPORT_DIR=exports/iphone_backups/$(date +%b_%d_%Y)
mkdir -p "$EXPORT_DIR"
echo "===================================="
echo "=== Starting Backup of iphone at $(date)"
echo "===================================="
idevicebackup2 -d backup --full $EXPORT_DIR
