import time
import boto3

def create_snapshot_handler(event, context):
	print 'Region: %s' % event['region']
	accountId = context.invoked_function_arn.split(':')[4]
	ec2 = boto3.resource('ec2', region_name=event['region'])

	volumes = ec2.volumes.all()
	for volume in volumes:
		if len(volume.attachments) > 0:
			print 'Snapshot from EBS volume %s on instance %s - Initiaded' % (volume.id, volume.attachments[0]['InstanceId'])

			description = 'Instance:%s, Volume:%s, Partition:%s' % (volume.attachments[0]['InstanceId'], volume.id, volume.attachments[0]['Device'])

			snapshot = volume.create_snapshot(Description=description)

			if volume.tags is not None:
				snapshot.create_tags(Tags=volume.tags)

			print 'Snapshot from EBS volume %s on instance %s - Completed' % (volume.id, volume.attachments[0]['InstanceId'])

			time.sleep(2)
	clean_snapshot(ec2, accountId)


def clean_snapshot(ec2, accountId):
	filters = [{'Name': 'tag-key', 'Values': ['Backup']},{'Name': 'tag-value', 'Values': ['false']}]
	snapshots = ec2.snapshots.filter(OwnerIds=[accountId], Filters=filters, MaxResults=500)
	for snapshot in snapshots:
		snapshot_id = snapshot.id
		snapshot_volume = snapshot.volume_id
		print 'Snapshot %s from EBS volume %s - Deleted' % (snapshot_id, snapshot_volume)
		try:
			snapshot.delete()
		except Exception as e:
			pass