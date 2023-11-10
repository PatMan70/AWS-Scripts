import boto3
from datetime import datetime, timedelta

# Initialize the EC2 resource
ec2 = boto3.resource('ec2')

# Define the retention periods
yearly_retention = 1
monthly_retention = 12
daily_retention = 1

# Define the snapshot tags
yearly_tag = {'Key': 'Retention', 'Value': 'yearly'}
monthly_tag = {'Key': 'Retention', 'Value': 'monthly'}
daily_tag = {'Key': 'Retention', 'Value': 'daily'}

# Function to delete excess snapshots
def delete_excess_snapshots(snapshot_dict, retention_count, exclude_descriptions):
    excess_snapshots = sorted(snapshot_dict.values(), key=lambda x: x.start_time, reverse=True)[retention_count:]
    for snapshot in excess_snapshots:
        if snapshot.description not in exclude_descriptions:
            snapshot.delete()

# Get all snapshots in the account
snapshots = list(ec2.snapshots.all())

# Sort snapshots by start time
snapshots.sort(key=lambda x: x.start_time)

# Define dictionaries to store snapshots by retention period
yearly_snapshots = {}
monthly_snapshots = {}
daily_snapshots = {}

# Group snapshots by retention period
for snapshot in snapshots:
    for tag in snapshot.tags:
        if tag == yearly_tag:
            yearly_snapshots[snapshot.id] = snapshot
        elif tag == monthly_tag:
            monthly_snapshots[snapshot.id] = snapshot
        elif tag == daily_tag:
            daily_snapshots[snapshot.id] = snapshot

# Delete excess yearly snapshots
delete_excess_snapshots(yearly_snapshots, yearly_retention, 
                        [s.description for s in monthly_snapshots.values()] + 
                        [s.description for s in daily_snapshots.values()])

# Delete excess monthly snapshots
delete_excess_snapshots(monthly_snapshots, monthly_retention,
                        [s.description for s in daily_snapshots.values()])

# Delete excess daily snapshots
delete_excess_snapshots(daily_snapshots, daily_retention, [])

# Create new snapshots for each volume
for volume in ec2.volumes.all():
    volume.create_snapshot(Description=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                           Tags=[daily_tag, monthly_tag, yearly_tag])
