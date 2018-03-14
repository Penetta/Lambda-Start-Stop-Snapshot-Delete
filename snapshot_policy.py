{
    "Version": "2012-10-17",
    "Id": "default",
    "Statement": [
        {
            "Sid": "automate-stack-deloitte-premmia-PermissionForEventsToInvokeCreateSnapshotFunction-1LL51VD0EXF74",
            "Effect": "Allow",
            "Principal": {
                "Service": "events.amazonaws.com"
            },
            "Action": "lambda:InvokeFunction",
            "Resource": "arn:aws:lambda:us-east-1:672052182609:function:CreateSnapshot",
            "Condition": {
                "ArnLike": {
                    "AWS:SourceArn": "arn:aws:events:us-east-1:672052182609:rule/create_snapshot_daily"
                }
            }
        }
    ]
}